<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" />
<xsl:template match="/">
 
<!-- Authors: chm, jus, sag -->
 
<!--/////////////////////////////////////////////////////////////////////////-->
<!--/// define the name of the input file ///////////////////////////////////-->
<!--/////////////////////////////////////////////////////////////////////////-->
<xsl:variable name="inputfilename"><xsl:text>input.xml</xsl:text></xsl:variable>
 
<!-- Loop over all elements named "set" from reference xml-file -->
<xsl:for-each select = "/experiment/set">
 
  <!-- Define path here -->
  <xsl:variable name="path">/fshome/tde/test/calctemp/<xsl:value-of select="./@path"/>/input.xml</xsl:variable>

 <!-- Write document at Path $path -->
  <xsl:document href="{$path}" method="xml" indent="yes">
 <xsl:comment>
 This file is generated with XSLTPROC using a template file and a reference file
 All parameters from the set filled in by XSLTPROC are listed below:
<!-- list all attributes in input file -->
<xsl:for-each select="./@*">
<xsl:text> </xsl:text>  
<xsl:value-of select="name()"/><xsl:text> </xsl:text>
<xsl:value-of select="."/><xsl:text>
>
</xsl:text>
<xsl:value-of select="$path"/>
</xsl:for-each><xsl:text></xsl:text>  
</xsl:comment>
<!-- ////////////////////////////////////////////////////////////////////////-->
<!-- /// The input file begins here /////////////////////////////////////////-->
<!-- ////////////////////////////////////////////////////////////////////////-->
 
<input xsi:noNamespaceSchemaLocation="excitinginput.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsltpath="./" scratchpath="/tmp/chm/1">
<title>
<xsl:text> </xsl:text>
<xsl:value-of select="position()"/>
</title>
<structure>
<xsl:attribute name="speciespath">/home/tde/exciting/species</xsl:attribute>
<xsl:element name="crystal">
 <xsl:attribute name="scale"><xsl:value-of select="@scale"/></xsl:attribute>

<basevect>1  1  0</basevect>
<basevect>1  0  1</basevect>
<basevect>0  1  1</basevect>
</xsl:element>
<species speciesfile="Al.xml">
<atom coord="0.0  0.0  0.0" bfcmt="0.0  0.0  0.0"></atom>
</species>
</structure>
 
<groundstate vkloff="0.5  0.5  0.5"   mixer="msec">
  <xsl:attribute name="ngkgrid"><xsl:value-of select="@ngkgrid"/></xsl:attribute>
  <xsl:attribute name="rgkmax"><xsl:value-of select="@rgkmax"/></xsl:attribute>
</groundstate>
</input>
 
<!-- ////////////////////////////////////////////////////////////////////////-->
<!-- /// The input file ends here ///////////////////////////////////////////-->
<!-- ////////////////////////////////////////////////////////////////////////-->
 
</xsl:document>
</xsl:for-each>
</xsl:template>
</xsl:stylesheet>