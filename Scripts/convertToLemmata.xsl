<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    <xsl:output method="xml" indent="yes"/>
    <xsl:template match="TEI.2">
        <TEI.2>
            <xsl:copy-of select="teiHeader"/>
            <text>
                <body>
                    <xsl:for-each select="text/body/sentence">
                        <sentence>
                            <xsl:attribute name="id">
                                <xsl:value-of select="./@id" />
                            </xsl:attribute>
                            <xsl:attribute name="location">
                                <xsl:value-of select="./@location" />
                            </xsl:attribute>
                            <xsl:for-each select="./word">
                                   <word>
                                       <xsl:attribute name="id">
                                           <xsl:value-of select="./@id" />
                                       </xsl:attribute>
                                       <xsl:attribute name="lemma">
                                           <xsl:value-of select="./lemma[1]/@entry" />
                                       </xsl:attribute>
                                   </word>
                            </xsl:for-each>
                        </sentence>
                    </xsl:for-each>
                </body>
            </text>
        </TEI.2>
    </xsl:template>
</xsl:stylesheet>