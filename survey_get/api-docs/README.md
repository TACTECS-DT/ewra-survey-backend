API Collection for Frontend Team
📥 Importing the Collection and Environment

    Open Postman.

    Click Import → select the provided .json files:

        Collection files: (no need to rename)

        Environment file: (no need to rename)

✅ No need to rename files — everything will be recognized directly.

    After importing, select the correct environment from the top right dropdown in Postman.

📤 Exporting (If Needed)

If you update requests or environments:

    Right-click the Collection → Export → choose 2.1 format (recommended).

    Right-click the Environment → Export.

🔐 Authentication Overview
API (Mobile, Client Apps)

    Authentication Type: JWT (JSON Web Token)

    Process:

        Use the JWT Login request (inside the  Login/Logout collection).

        It will return:

            access_token

            refresh_token

        The access_token will be automatically saved into the environment ({{auth_token}}).

        All other API requests will auto-use Authorization: Bearer {{auth_token}} in headers.

    Refreshing Token:

        When the access token expires, use the Refresh Token request to get a new access token.

Admin (Dashboard, CMS)

    Authentication Type: Session-Based (Cookie)

    Process:

        Use the Admin Login request.

        Successful login will set a session cookie.

         All Admin panel pages will use that session automatically without needing JWT. (--->this is for internal  pages not the end points -->all end points will be under JWT auth)

🌐 Environment Variables

    {{base_url}} → Points to your backend server address (example: https://api.dev.example.com).

    Important:

        Change base_url when switching between Development, Staging, or Production servers.

        You do NOT need to manually change each request URL — just update the environment variable.

🧪 Sample Responses

    Inside each request in the collection, you’ll find a sample response example.

    These examples show:

        Typical data structure.

        Expected fields and values...(soon)

        Standard error formats...(soon)

✅ This helps frontend developers to understand exactly what the backend will return without guessing.
⚡ Quick Notes

    Pagination parameters: ?page=1

    Common HTTP Status codes:

        200 OK → Success

        400 Bad Request → Validation error

        401 Unauthorized → Auth failed

        403 Forbidden → No permission

        404 Not Found → Missing resource