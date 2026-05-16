# System Overview & Features Guide

## Core Features

### 1. User Authentication & Profile
- **Secure Authentication**: Built using Django's standard auth system with customized modern templates.
- **Profile Management**: Users can update their Bio and Profile Picture.
- **Security**: Includes both "Forgot Password" (via Email) and "Change Password" (Logged-in) features.

### 2. Blog Management (CRUD)
- **Content Creation**: Full Markdown support for rich text blog posts.
- **Categorization**: Dynamically filter posts by category (e.g., Tech, Lifestyle).
- **Ownership**: Strict permission checks—users can only modify their own content.

### 3. Interactive Comment System
- **Public Engagement**: Supports both authenticated and anonymous comments.
- **Threaded Conversations**: Multi-level reply system allowing users to respond directly to specific comments.

### 4. Advanced Search & Discovery
- **Prioritized Ranking**: Search results are intelligently ranked:
    1. Matches in **Author** names (Highest)
    2. Matches in **Post Titles**
    3. Matches in **Post Content**
- **AJAX Search**: Results update instantly without page reloads.

---

## Enhancements 

- **Real-Time Polling**: Comments and view counts update automatically in the background without refreshing the page.
- **Skeleton Loading**: Implemented shimmer-effect placeholders to prevent layout shifts and "white flashes" during load.
- **Web Share API**: Native device sharing support for mobile and desktop.
- **Bookmark System**: Users can save stories to a private "Saved Stories" list in their profile.
- **Real Email Integration**: Configured with SMTP to send actual password reset emails.
- **Modern UI**: Fully responsive, dark-mode compatible interface with glassmorphism aesthetics and scroll-reveal animations.

---

## Tech Stack
- **Backend**: Django 5.0 (Python)
- **Database**: SQLite3
- **Frontend**: Bootstrap 5, Vanilla JS, CSS3 (Custom Variables)
- **Markdown Processing**: Marked.js
