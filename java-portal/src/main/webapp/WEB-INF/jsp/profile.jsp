<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><c:out value="${student.name}"/> - Student Profile</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/portal.css">
</head>
<body>

    <header class="portal-navbar">
        <a href="${pageContext.request.contextPath}/students" class="portal-brand">
            <div class="brand-badge">J</div>
            <div class="brand-text">
                <h1>Student Admission Portal</h1>
                <span>Academic Record Details</span>
            </div>
        </a>

        <div class="nav-actions">
            <a href="${pageContext.request.contextPath}/students" class="btn-secondary" style="font-size: 0.85rem;">
                &larr; Back to Student Registry
            </a>
            <a href="${pageContext.request.contextPath}/logout" class="btn-nav-logout">Logout</a>
        </div>
    </header>

    <main class="portal-main">

        <div class="profile-grid">
            
            <!-- Left Column: Avatar & Quick Summary Card -->
            <div class="profile-avatar-card">
                <div class="large-avatar">
                    <c:choose>
                        <c:when test="${not empty student.profileImage}">
                            <img src="${pageContext.request.contextPath}/document?profile=<c:out value='${student.profileImage}'/>" 
                                 alt="<c:out value='${student.name}'/>"
                                 onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
                            <span class="large-avatar-fallback" style="display: none;">
                                ${student.name.substring(0, 1)}
                            </span>
                        </c:when>
                        <c:otherwise>
                            <span class="large-avatar-fallback">
                                ${student.name.substring(0, 1)}
                            </span>
                        </c:otherwise>
                    </c:choose>
                </div>

                <h2 style="font-size: 1.25rem; font-weight: 700; color: var(--text-primary);">
                    <c:out value="${student.name}"/>
                </h2>
                <p style="color: var(--primary); font-weight: 600; font-size: 0.95rem; margin-top: 0.2rem;">
                    <c:out value="${student.rollNumber}"/>
                </p>

                <div style="margin-top: 0.75rem;">
                    <c:choose>
                        <c:when test="${student.status eq 'Approved'}">
                            <span class="badge badge-approved" style="font-size: 0.82rem; padding: 0.35rem 0.85rem;">Approved Application</span>
                        </c:when>
                        <c:when test="${student.status eq 'Pending'}">
                            <span class="badge badge-pending" style="font-size: 0.82rem; padding: 0.35rem 0.85rem;">Under Review</span>
                        </c:when>
                        <c:otherwise>
                            <span class="badge badge-rejected" style="font-size: 0.82rem; padding: 0.35rem 0.85rem;"><c:out value="${student.status}"/></span>
                        </c:otherwise>
                    </c:choose>
                </div>

                <ul class="profile-meta-list">
                    <li>
                        <span class="label">Degree Program</span>
                        <span class="value" style="text-align: right;"><c:out value="${student.course}"/></span>
                    </li>
                    <li>
                        <span class="label">Email Address</span>
                        <span class="value"><c:out value="${student.email}"/></span>
                    </li>
                    <li>
                        <span class="label">Registered On</span>
                        <span class="value">
                            <c:out value="${student.registrationDate}"/>
                        </span>
                    </li>
                </ul>

                <div style="margin-top: 1.5rem;">
                    <a href="http://localhost/student-admission-portal/php-admin/edit_student.php?id=${student.id}" 
                       class="btn-secondary" style="width: 100%; justify-content: center; font-size: 0.85rem;" target="_blank">
                        Edit in PHP Admin &rarr;
                    </a>
                </div>
            </div>

            <!-- Right Column: Uploaded Documents & Metadata -->
            <div>
                
                <div class="content-card">
                    <div class="content-card-header">
                        <div>
                            <h3 class="content-card-title">Associated Academic Documents &amp; Credentials</h3>
                            <p style="font-size: 0.82rem; color: var(--text-secondary); margin-top: 0.2rem;">
                                Files streamed dynamically via <code>DocumentStreamServlet</code> with path-traversal prevention.
                            </p>
                        </div>
                    </div>

                    <div class="table-responsive">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Category</th>
                                    <th>Original Filename</th>
                                    <th>MIME Type</th>
                                    <th>File Size</th>
                                    <th>Upload Date</th>
                                    <th style="text-align: right;">Stream Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <c:choose>
                                    <c:when test="${not empty documents}">
                                        <c:forEach var="doc" items="${documents}">
                                            <tr>
                                                <td>
                                                    <span class="badge badge-category">
                                                        <c:out value="${doc.documentCategory.replace('_', ' ')}"/>
                                                    </span>
                                                </td>

                                                <td>
                                                    <div style="font-weight: 600; color: var(--text-primary);">
                                                        <c:out value="${doc.originalFilename}"/>
                                                    </div>
                                                </td>

                                                <td>
                                                    <code style="font-size: 0.8rem; background: #f1f5f9; padding: 0.15rem 0.4rem; border-radius: 4px;">
                                                        <c:out value="${doc.mimeType}"/>
                                                    </code>
                                                </td>

                                                <td>
                                                    <span style="color: var(--text-secondary); font-size: 0.85rem;">
                                                        <c:out value="${doc.formattedSize}"/>
                                                    </span>
                                                </td>

                                                <td>
                                                    <span style="color: var(--text-muted); font-size: 0.82rem;">
                                                        <c:out value="${doc.uploadedAt}"/>
                                                    </span>
                                                </td>

                                                <td style="text-align: right;">
                                                    <div style="display: inline-flex; gap: 0.4rem;">
                                                        <a href="${pageContext.request.contextPath}/document?id=${doc.id}" 
                                                           target="_blank" class="btn-secondary" 
                                                           style="padding: 0.3rem 0.65rem; font-size: 0.78rem;" title="View file in browser">
                                                            View
                                                        </a>
                                                        <a href="${pageContext.request.contextPath}/document?id=${doc.id}&download=true" 
                                                           class="btn-primary" 
                                                           style="padding: 0.3rem 0.65rem; font-size: 0.78rem;" title="Force download">
                                                            Download
                                                        </a>
                                                    </div>
                                                </td>
                                            </tr>
                                        </c:forEach>
                                    </c:when>
                                    <c:otherwise>
                                        <tr>
                                            <td colspan="6">
                                                <div class="empty-state" style="padding: 2.5rem 1rem;">
                                                    <h4>No Additional Documents Found</h4>
                                                    <p>This candidate has not uploaded extra identity proofs or marksheets yet.</p>
                                                </div>
                                            </td>
                                        </tr>
                                    </c:otherwise>
                                </c:choose>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- PHP Admin Cross-Navigation Notice -->
                <div style="background-color: #f1f5f9; border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 1.25rem; font-size: 0.88rem; color: var(--text-secondary);">
                    <strong style="color: var(--text-primary);">Integration Note:</strong> This profile view is powered by the Jakarta Servlet/JSP engine running on Tomcat. All updates made via the PHP Admin Panel or Student Registration form are instantly visible here through shared MySQL database state.
                </div>

            </div>

        </div>

    </main>

    <footer class="portal-footer">
        Student Admission Portal &bull; CO5 Jakarta Servlets &amp; JSP &bull; Apache Tomcat
    </footer>

</body>
</html>
