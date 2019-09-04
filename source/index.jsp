<%-- 
	NAME:   INDEX.JSP
	DESC:   RETRIEVE HTTP REQUEST HEADERS USING JSP
	DATE:   01-09-2019
	LANG:   JSP
	AUTHOR: LAGUTIN R.A.
	EMAIL:  RLAGUTIN@MTA4.RU
--%>

<%@page import="java.util.Enumeration"%>
<%@page import="java.util.Iterator"%>
<%@page import="java.util.Set"%>
<%@page import="weblogic.management.runtime.ServerRuntimeMBean"%>
<%@page import="java.net.UnknownHostException"%>
<%@page import="java.net.InetAddress"%>
<%@page import="java.net.URLDecoder"%>
<%@page import="weblogic.management.*"%>

<%
    String hostname, serverAddress;
    hostname = "error";
    serverAddress = "error";
    try {
        InetAddress inetAddress;
        inetAddress = InetAddress.getLocalHost();
        hostname = inetAddress.getHostName();
        serverAddress = inetAddress.toString();
    } catch (UnknownHostException e) {
        e.printStackTrace();
    }
%>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>WebLogic Server on Docker - Request Informationo</title>
	<style>
		body {
		background-color: white;
		text-align: left;
		padding: 50px;
		font-family: 'Open Sans','Helvetica Neue',Helvetica,Arial,sans-serif;
		}
	</style>
    </head>
    <body>

<%
	Integer hitsCount = (Integer)application.getAttribute("hitCounter");
	if( hitsCount ==null || hitsCount == 0 ) {
		hitsCount = 1;
	} else {
		hitsCount += 1;
	}
	application.setAttribute("hitCounter", hitsCount);
%>

	<h2>Hello from <font color='#337ab7'>WebLogic Server on Docker</font></h2>
	<b>Visits:</b> <%=hitsCount%><br>
	<br>
	<b>Request method:</b> <%=request.getMethod()%><br>
	<b>Request URI:</b> <%=request.getRequestURI()%><br>
	<b>Request protocol:</b> <%=request.getProtocol()%><br>
	<b>Remote Host:</b> <%=request.getRemoteHost()%><br>
	<b>Remote Address:</b> <%=request.getRemoteAddr()%><br>
	<br>
	<b>getVirtualServerName():</b> <%= request.getServletContext().getVirtualServerName() %><br>
	<b>InetAddress.hostname:</b> <%=hostname%><br>
	<b>InetAddress.serverAddress:</b> <%=serverAddress%><br>
	<b>getLocalAddr():</b> <%=request.getLocalAddr()%><br>
	<b>getLocalName():</b> <%=request.getLocalName()%><br>
	<b>getLocalPort():</b> <%=request.getLocalPort()%><br>
	<b>getServerName():</b> <%=request.getServerName()%><br>
	<b>WLS Server Name:</b> <%=System.getProperty("weblogic.Name")%><br>
	<br><hr>
	<h4>Headers:</h4>"

<%
        Enumeration enumeration = request.getHeaderNames();
        while (enumeration.hasMoreElements()) {
                String name = (String) enumeration.nextElement();
                String value = request.getHeader(name);
                out.print(name + ": " + value +"<br>");
        }
%>

    </body>
</html>
