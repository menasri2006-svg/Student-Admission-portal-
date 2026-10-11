<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Java Admin Portal - Student Admission Management</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/portal.css">
</head>
<body>

    <div class="login-wrapper">
        <div class="login-card">
            
            <div class="login-header">
                <div style="display: flex; justify-content: center;">
                    <div class="brand-badge" style="width: 48px; height: 48px; font-size: 1.5rem;">J</div>
                </div>
                <h2>Java Admin Portal</h2>
                <p>Jakarta / Tomcat 8.5 Servlet &amp; JSP Architecture</p>
            </div>

            <!-- Error Banner -->
            <c:if test="${not empty errorMessage}">
                <div class="alert alert-danger" role="alert">
                    <span>&#9888;</span>
                    <div><c:out value="${errorMessage}"/></div>
                </div>
            </c:if>

            <!-- Success Banner -->
            <c:if test="${not empty successMessage}">
                <div class="alert alert-success" role="alert">
                    <span>&#10003;</span>
                    <div><c:out value="${successMessage}"/></div>
                </div>
            </c:if>

            <form action="${pageContext.request.contextPath}/login" method="POST">
                <div class="form-group">
                    <label for="username" class="form-label">Admin Username</label>
                    <input type="text" id="username" name="username" class="form-control" 
                           value="<c:out value='${username}' default='admin'/>" required autofocus autocomplete="username">
                </div>

                <div class="form-group">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" id="password" name="password" class="form-control" 
                           placeholder="Enter administrator password" required autocomplete="current-password">
                </div>

                <button type="submit" class="btn-primary btn-block">
                    Sign In to Portal
                </button>
            </form>

            <div style="margin-top: 1.75rem; text-align: center; border-top: 1px solid var(--border-color); padding-top: 1rem; font-size: 0.82rem; color: var(--text-secondary);">
                <p>Default credentials: <strong>admin</strong> / <strong>Password@123</strong></p>
                <div style="margin-top: 0.5rem; display: flex; justify-content: center; gap: 1rem;">
                    <a href="http://localhost/student-admission-portal/registration/" style="color: var(--primary); text-decoration: none;">&larr; Registration Form</a>
                    <a href="http://localhost/student-admission-portal/php-admin/login.php" style="color: var(--accent); text-decoration: none;">PHP Admin &rarr;</a>
                </div>
            </div>

        </div>
    </div>

    <footer class="portal-footer">
        Student Admission Portal &bull; CO5 Jakarta Servlets &amp; JSP &bull; Apache Tomcat
    </footer>

</body>
</html>
