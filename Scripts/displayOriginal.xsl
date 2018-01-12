<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
<xsl:output method="text" omit-xml-declaration="yes" indent="no"/>
<xsl:template match="teiHeader"/>
    <xsl:template match="body">
        <xsl:for-each select="sentence"><xsl:value-of select="concat(./@id, ' (', ./@location,'): ')"/>
            <xsl:for-each select="./*">
                <xsl:choose>
                    <xsl:when test="./@form">
                        <xsl:value-of select="./@form"/>
                        <xsl:if test="not(following-sibling::*[1]/local-name()='punct')">
                            <xsl:text> </xsl:text>
                        </xsl:if>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:if test="./@mark = '('">
                        <xsl:text> </xsl:text>
                        </xsl:if>
                        <xsl:value-of select="./@mark"/>
                        <xsl:if test="./@mark != '('">
                            <xsl:text> </xsl:text>
                        </xsl:if>
                    </xsl:otherwise>    
                </xsl:choose>
            </xsl:for-each>
            <xsl:text>
</xsl:text>
        </xsl:for-each>
        
    </xsl:template>
</xsl:stylesheet>