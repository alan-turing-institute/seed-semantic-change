package model

import (
    "dynamic-senses_release/util"
    "fmt"
)

func (m *Model)Print() {
    fmt.Println("\n======================")
    m.Print_category_proportions()
    m.Print_category_feature_counts()
    fmt.Println("\n======================")
}

func (m *Model) Print_category_proportions() {
    fmt.Println("Category Proportions")
    for g:=0 ; g<m.Parameters.Num_genres ; g++ {
        fmt.Println(m.N_k[g][0].String())
    }
    fmt.Println("\n-------------------\n")
}


func (m *Model) Print_category_feature_counts() {
    fmt.Println("Category Feature Counts")
    for k:=0 ; k<m.Parameters.Num_categories ; k++ {
        fmt.Println(m.N_k_f[k].String())
    }
    fmt.Println("\n-------------------\n")
}



/* ********************************************** *
 * **********    PRINTING CLUSTERS   ************ *
 * ********************************************** */
func (m *Model) Print_categories(topN int, conceptStrings, featureStrings map[int]string) (out string) {
    fmt.Println("===============  per type  ===============")
    out += fmt.Sprintln("===============  per type  ===============")
    for g:=0 ; g<m.Parameters.Num_genres ; g++ {
      for k:=0 ; k<m.Parameters.Num_categories ; k++ {
          fmt.Printf("Featuretype=%d  \n", k)
          for t:=0 ; t<m.Parameters.Num_timestamps ; t++ {
              fmt.Print(m.Phi[g][0].Get(t,k), " ")
              out +=  fmt.Sprint(m.Phi[g][0].Get(t,k), " ")
              out += m.print_top_features_k_t(k, t, topN, featureStrings, "p_w_given_t,s")
          }
          fmt.Print("p(w|s) = sum_t P(w|t,s) ")
          out += fmt.Sprint("p(w|s) = sum_t P(w|t,s)")
          out += m.print_top_features_k_t(k, -1, topN, featureStrings, "p_w_given_s")+"\n"
          fmt.Println("\n")
      }
    }
    fmt.Println()
    fmt.Println("===============  per time  ===============")
    out += fmt.Sprintln("===============  per time  ===============")
    for t:=0 ; t<m.Parameters.Num_timestamps ; t++ {
      for g:=0 ; g<m.Parameters.Num_genres ; g++ {
        fmt.Printf("Time=%d  \n", t)
        out += fmt.Sprintf("Time=%d  \n", t)
        for k:=0 ; k<m.Parameters.Num_categories ; k++ {
            fmt.Print(m.Phi[g][0].Get(t,k), " ")
            out += fmt.Sprint(m.Phi[g][0].Get(t,k), " ")
            out += m.print_top_features_k_t(k, t, topN, featureStrings, "p_w_given_t,s")
        }

        fmt.Println()
        out += fmt.Sprintln()
      }
    }
    return
}

func (m *Model) print_top_features_k_t(k, t, topN int, featureStrings map[int]string, mode string) (out string) {

    values, topFeatures := m.Top_features_given_k_t(k, t, mode)

    fmt.Printf("  T=%d,K=%d:  ", t,k)
    out += fmt.Sprintf("  T=%d,K=%d:  ", t,k)
    cnt:=0
    for f:=len(topFeatures)-1 ; f>=0&&cnt<topN ; f-- {
        fmt.Printf("%s (%.3f) ; ", featureStrings[topFeatures[f]], values[f])
        out += fmt.Sprintf("%s (%.3f) ; ", featureStrings[topFeatures[f]], values[f])
        cnt++
    }
    fmt.Println()
    out += fmt.Sprintln()
    return
}



func (m *Model) Print_top_features_k_t(k, t, topN int, featureStrings map[int]string) (out string) {
    values, topFeatures := m.Top_features_given_k_t(k, t, "p_w_given_t,s")

    cnt:=0

    for f:=len(topFeatures)-1 ; f>=0 && (cnt<topN || topN<0) && values[f]>0.0 ; f-- {
        out += fmt.Sprintf(" %s", featureStrings[topFeatures[f]])
        cnt++
    }
    out += fmt.Sprintln()
    return
}



func (m *Model) Print_gnuplot_datfile(topN int, conceptStrings, featureStrings map[int]string) (out string) {
    /* line 1: print characteristic words */
    out += "time "
    for k:=0 ; k<m.Parameters.Num_categories ; k++ {
        out += `"`
        out += m.print_top_words(k, -1, topN, featureStrings, "p_w_given_s")
        out += `" `
    }
    out += "\n"
    /* lines 2ff: print time p(k|time) for all k*/
    for t:=0 ; t<m.Parameters.Num_timestamps ; t++ {
        out += fmt.Sprintf("%d ", t)
        for g:=0 ; g<m.Parameters.Num_genres ; g++ {
          for k:=0 ; k<m.Parameters.Num_categories ; k++ {
              out += fmt.Sprint(m.Phi[g][0].Get(t,k), " ")
          }
        }

        out += fmt.Sprintln()
    }
    return
}


func (m *Model) print_top_words(k, t, topN int, featureStrings map[int]string, mode string) (out string) {

    _, topFeatures := m.Top_features_given_k_t(k, t, mode)
    cnt:=0
    for f:=len(topFeatures)-1 ; f>=0&&cnt<topN ; f-- {
        out += fmt.Sprintf("%s ", featureStrings[topFeatures[f]])
        cnt++
    }
    return
}


func (m *Model) Print_hard_senses(s, t int, topN int, featureStrings map[int]string) (out string) {
    hard_senses := m.hard_sense_clustering(t)
    if s < 0 {
        for ss:=0 ; ss<m.Parameters.Num_categories ; ss++ {
            hard_senses_sorted := util.SortIntKeysByFloatValues(hard_senses[ss])
            for f:=0 ; f<len(hard_senses_sorted) && (f<topN || topN<0) && hard_senses_sorted[f].Value > 0.0 ; f++ {
                out += fmt.Sprintf(" %s", featureStrings[hard_senses_sorted[f].Key])
            }
            out += fmt.Sprintln()
        }
    } else {
        hard_senses_sorted := util.SortIntKeysByFloatValues(hard_senses[s])
        for f:=0 ; f<len(hard_senses_sorted) && (f<topN || topN<0) && hard_senses_sorted[f].Value > 0.0 ; f++ {
            out += fmt.Sprintf(" %s", featureStrings[hard_senses_sorted[f].Key])
        }
        out += fmt.Sprintln()
    }
    return
}
