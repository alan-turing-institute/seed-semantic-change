<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
<xsl:output method="text" omit-xml-declaration="yes" indent="no"/>
<xsl:template match="teiHeader"/>
    <xsl:template match="body">
        <xsl:for-each select="sentence"><xsl:value-of select="concat(./@id, ' (', ./@location,'): ')"/>
            <xsl:for-each select="./word">
                <xsl:value-of select="./@lemma"/><xsl:text> </xsl:text>
            </xsl:for-each>
            <xsl:text>
</xsl:text>
        </xsl:for-each>
        
    </xsl:template>
</xsl:stylesheet>