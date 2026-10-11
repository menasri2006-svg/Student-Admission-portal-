        </main>
    </div>

    <!-- Confirm Dialog Script for Safe Deletion -->
    <script>
        function confirmDelete(studentName, rollNumber) {
            return confirm("Are you sure you want to permanently delete student record:\n\n" + 
                           studentName + " (" + rollNumber + ")\n\n" +
                           "This will also safely delete all associated documents from disk. This action cannot be undone.");
        }
        function confirmDocDelete(docName) {
            return confirm("Are you sure you want to permanently delete this document:\n\n" + 
                           docName + "\n\nThis action cannot be undone.");
        }
    </script>
</body>
</html>
