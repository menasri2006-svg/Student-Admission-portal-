<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registered Students - Java Admission Portal</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/portal.css">
</head>
<body>

    <!-- Main Navigation Bar -->
    <header class="portal-navbar">
        <a href="${pageContext.request.contextPath}/students" class="portal-brand">
            <div class="brand-badge">J</div>
            <div class="brand-text">
                <h1>Student Admission Portal</h1>
                <span>Java Servlet &amp; JSP Registry</span>
            </div>
        </a>

        <div class="nav-actions">
            <div class="admin-greeting">
                Welcome, <strong><c:out value="${sessionScope.adminUser.fullName}" default="Administrator"/></strong>
            </div>
            <a href="http://localhost/student-admission-portal/registration/" class="btn-secondary" style="font-size: 0.8rem; padding: 0.35rem 0.75rem;" target="_blank">Student Form</a>
            <a href="${pageContext.request.contextPath}/logout" class="btn-nav-logout">Logout</a>
        </div>
    </header>

    <main class="portal-main">

        <!-- Error notification if database failure occurred -->
        <c:if test="${not empty dbError}">
            <div class="alert alert-danger" role="alert">
                <span>&#9888;</span>
                <div><c:out value="${dbError}"/></div>
            </div>
        </c:if>

        <!-- KPI Statistic Cards -->
        <div class="stats-grid">
            <div class="stat-card">
                <span class="stat-card-title">Total Enrolled Students</span>
                <span class="stat-card-value"><c:out value="${totalStudents}" default="0"/></span>
                <span class="stat-card-subtitle">Verified in MySQL `students` table</span>
            </div>

            <div class="stat-card">
                <span class="stat-card-title">Total Uploaded Documents</span>
                <span class="stat-card-value"><c:out value="${totalDocs}" default="0"/></span>
                <span class="stat-card-subtitle">Stored certificates &amp; ID proofs</span>
            </div>

            <div class="stat-card">
                <span class="stat-card-title">Academic Departments</span>
                <span class="stat-card-value">
                    <c:choose>
                        <c:when test="${not empty courseSummary}">
                            ${courseSummary.size()}
                        </c:when>
                        <c:otherwise>0</c:otherwise>
                    </c:choose>
                </span>
                <span class="stat-card-subtitle">Active degree &amp; postgraduate programs</span>
            </div>
        </div>

        <!-- Registered Students Table Card -->
        <div class="content-card">
            
            <div class="content-card-header">
                <div>
                    <h2 class="content-card-title">Student Registry &amp; Admission Records</h2>
                    <span style="font-size: 0.82rem; color: var(--text-secondary);">
                        Data retrieved via JDBC PreparedStatement and rendered using JSTL &amp; Expression Language (EL).
                    </span>
                </div>

                <!-- Live Search Form -->
                <form action="${pageContext.request.contextPath}/students" method="GET" class="search-form">
                    <input type="text" name="search" class="input-search" 
                           placeholder="Search by name, roll, course..." 
                           value="<c:out value='${searchQuery}'/>">
                    <button type="submit" class="btn-primary">Search</button>
                    <c:if test="${not empty searchQuery}">
                        <a href="${pageContext.request.contextPath}/students" class="btn-secondary">Clear</a>
                    </c:if>
                </form>
            </div>

            <div class="table-responsive">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th style="width: 70px;">Avatar</th>
                            <th>Roll Number</th>
                            <th>Student Name</th>
                            <th>Academic Program</th>
                            <th>Email Address</th>
                            <th style="text-align: center;">Docs</th>
                            <th style="text-align: center;">Status</th>
                            <th style="text-align: right;">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <c:choose>
                            <c:when test="${not empty students}">
                                <c:forEach var="student" items="${students}">
                                    <tr>
                                        <!-- Profile Picture Streaming Tag -->
                                        <td>
                                            <div class="avatar-wrap">
                                                <c:choose>
                                                    <c:when test="${not empty student.profileImage}">
                                                        <img src="${pageContext.request.contextPath}/document?profile=<c:out value='${student.profileImage}'/>" 
                                                             alt="Avatar" class="avatar-img"
                                                             onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
                                                        <span class="avatar-fallback" style="display: none;">
                                                            ${student.name.substring(0, 1)}
                                                        </span>
                                                    </c:when>
                                                    <c:otherwise>
                                                        <span class="avatar-fallback">
                                                            ${student.name.substring(0, 1)}
                                                        </span>
                                                    </c:otherwise>
                                                </c:choose>
                                            </div>
                                        </td>

                                        <td>
                                            <strong style="color: var(--primary); font-size: 0.92rem;">
                                                <c:out value="${student.rollNumber}"/>
                                            </strong>
                                        </td>

                                        <td>
                                            <div style="font-weight: 600; color: var(--text-primary);">
                                                <c:out value="${student.name}"/>
                                            </div>
                                        </td>

                                        <td>
                                            <span style="color: var(--text-secondary); font-size: 0.88rem;">
                                                <c:out value="${student.course}"/>
                                            </span>
                                        </td>

                                        <td>
                                            <span style="color: var(--text-muted); font-size: 0.85rem;">
                                                <c:out value="${student.email}"/>
                                            </span>
                                        </td>

                                        <td style="text-align: center;">
                                            <span class="badge" style="background-color: #eff6ff; color: #1d4ed8;">
                                                ${student.documentCount} file(s)
                                            </span>
                                        </td>

                                        <td style="text-align: center;">
                                            <c:choose>
                                                <c:when test="${student.status eq 'Approved'}">
                                                    <span class="badge badge-approved">Approved</span>
                                                </c:when>
                                                <c:when test="${student.status eq 'Pending'}">
                                                    <span class="badge badge-pending">Pending</span>
                                                </c:when>
                                                <c:otherwise>
                                                    <span class="badge badge-rejected"><c:out value="${student.status}"/></span>
                                                </c:otherwise>
                                            </c:choose>
                                        </td>

                                        <td style="text-align: right;">
                                            <a href="${pageContext.request.contextPath}/profile?id=${student.id}" 
                                               class="btn-primary" style="padding: 0.35rem 0.85rem; font-size: 0.8rem;">
                                                View Profile &rarr;
                                            </a>
                                        </td>
                                    </tr>
                                </c:forEach>
                            </c:when>
                            <c:otherwise>
                                <tr>
                                    <td colspan="8">
                                        <div class="empty-state">
                                            <h3>No Student Records Found</h3>
                                            <p>No student applications match the query. Try adjusting your search keywords.</p>
                                        </div>
                                    </td>
                                </tr>
                            </c:otherwise>
                        </c:choose>
                    </tbody>
                </table>
            </div>

        </div>

    </main>

    <footer class="portal-footer">
        Student Admission Portal &bull; CO5 Jakarta Servlets &amp; JSP &bull; Apache Tomcat 8.5+ &bull; MySQL Shared Database
    </footer>

</body>
</html>
