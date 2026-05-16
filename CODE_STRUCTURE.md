# Django Blog Project Structure

This document outlines the file structure and architecture of the `blog_project`. The project uses a modular design with two primary applications: `blog` (for handling content) and `users` (for handling authentication and profiles).

## Project Root Directory (`d:\BITProject\`)

* **`README.md`**: Contains setup instructions, virtual environment configuration, and quick-start commands.
* **`requirements.txt`**: Lists all Python dependencies required to run the project (e.g., `Django>=5.0`, `Pillow`).
* **`CODE_STRUCTURE.md`**: This file, explaining the architecture of the project.

---

## Core Django Project (`blog_project/blog_project/`)

This directory contains the main configuration for the entire application.

* **`settings.py`**: The heart of the configuration. It registers the `blog` and `users` apps, configures the SQLite database, sets up paths for `templates`, `static`, and `media` directories, and defines the `LOGIN_REDIRECT_URL`.
* **`urls.py`**: The master router. It routes traffic to the admin panel (`/admin/`), routes root traffic (`/`) to the `blog` app, and routes `/users/` traffic to the `users` app. It also configures media serving for the development environment.
* **`wsgi.py` / `asgi.py`**: Entry points for web servers (like Gunicorn or Daphne) to serve the application in production.

---

## Blog Application (`blog_project/blog/`)

This app handles everything related to creating, reading, updating, and deleting blog posts, as well as categorizing them and managing comments.

* **`models.py`**:
  * `Post`: The core model for blog entries. Includes a `views` counter and a `likes` ManyToMany relationship.
  * `Category`: Manages post grouping.
  * `Comment`: Supports both registered and anonymous comments, with a self-referencing ForeignKey for nested replies.
  * `Bookmark`: Stores the relationship between users and their saved "read later" stories.
* **`views.py`**: Utilizes Django's Generic Class-Based Views for rapid development and clean code:
  * `PostListView`: Handles the home page, listing posts, pagination, category filtering, and the search bar functionality. It supports **AJAX requests** for instant, zero-reload search and category filtering.
  * `PostDetailView`: A complex view that handles individual post display, view incrementing, like toggling (AJAX), and the comment form.
  * `BookmarkToggleView`: An AJAX-specific view that allows users to save/unsave stories without a page refresh.
  * `upload_image`: A custom view that handles secure Markdown image uploads to the `media/post_images/` directory.
  * `PostCreateView`, `PostUpdateView`, `PostDeleteView`: Handle the creation, modification, and deletion of posts (restricted to logged-in users and post authors). Utilizes `PostForm` for consistent category selection logic.
* **`forms.py`**: Contains the `CommentForm` used to validate and sanitize incoming comments and replies.
* **`urls.py`**: Defines the URL patterns for the blog CRUD operations (e.g., `/post/<int:pk>/`, `/post/new/`).

---

## Users Application (`blog_project/users/`)

This app manages user accounts, authentication, and extending the default Django `User` model with additional profile information.

* **`models.py`**:
  * `Profile`: Extends the built-in `User` model using a OneToOne field. It adds an `image` field for profile pictures (requires Pillow) and a `bio` text field.
* **`views.py`**:
  * `register`: Handles new user signups using a custom registration form.
  * `profile`: A `@login_required` view that allows users to update their username, email, profile picture, and bio simultaneously.
* **`forms.py`**:
  * `UserRegisterForm`: Extends the default `UserCreationForm` to require an email address upon signup.
  * `UserUpdateForm` & `ProfileUpdateForm`: Forms used to validate user data updates on the profile page.
* **`urls.py`**: Routes authentication requests. It connects to custom views (`register`, `profile`) and utilizes Django's built-in `auth_views` for login, logout, and the entire password reset flow.

---

## Global Directories (`blog_project/`)

These directories sit at the root of the Django project and are shared across all apps.

### `templates/`
Configured in `settings.py` as a global template directory. It uses Bootstrap 5 for responsive design.
* **`base.html`**: The master template. Contains the global navigation, theme-switching logic, and the **Global Skeleton Preloader**.
* **`blog/`**:
  * `home.html`: Displays the list of posts, modern horizontal category chips, and a dynamic search bar. Implements **AJAX instant search** with debouncing and skeleton loading feedback.
  * `_post_list.html`: [NEW] A partial template used by AJAX requests to update the post container without a full page reload.
  * `post_detail.html`: Displays the full post content. Contains the **Live Polling** JavaScript that updates likes and comments every 10 seconds.
  * `_comment.html`: A partial template used for rendering comments and their recursive replies.
  * `post_form.html`: The form used for both creating and updating posts. Includes specialized logic for the category dropdown placeholder.
  * `post_confirm_delete.html`: A confirmation page before permanently deleting a post.
* **`users/`**:
  * `login.html`, `register.html`, `logout.html`: Authentication templates.
  * `profile.html`: A tabbed interface separating "My Stories", "Saved Stories", and "Account Settings".
  * `password_reset*.html`: Templates for the forgotten password email flow.
  * `password_change.html`: A secure form for logged-in users to update their password.

### `static/`
Contains static assets like custom CSS, JavaScript files, and site-wide images (e.g., a site logo).

### `media/`
Stores user-uploaded files. For example, when a user uploads a custom profile picture, it is saved into `media/profile_pics/`. Django is configured to serve these files during development via URL routing.
