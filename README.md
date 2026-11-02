# 🍲 Smilecook Recipe API

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Framework-Flask-black?logo=flask)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?logo=postgresql)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Educational Use Only](https://img.shields.io/badge/Purpose-Educational-blue)

A robust RESTful API built with **Python** and **Flask** that allows users to create, share, and discover recipes. This project features secure JWT authentication, user management, and full CRUD operations for recipes using a PostgreSQL database.

---

## ✨ Features

*   **User Authentication:** Secure registration and login using JWT (JSON Web Tokens).
*   **User Profiles:** View public profiles and access private "Me" endpoints for personal data.
*   **Recipe Management:** Create, read, update, and delete recipes.
*   **Publishing System:** Toggle recipes between draft and published states.
*   **Advanced Security:** Token refresh mechanisms, token blocklisting (logout), and password hashing.
*   **Database Migrations:** Fully integrated with Flask-Migrate for safe database schema updates.

---

## 🛠️ Tech Stack

*   **Language:** Python 3.x
*   **Framework:** Flask, Flask-RESTful
*   **Database:** PostgreSQL
*   **ORM:** Flask-SQLAlchemy
*   **Authentication:** Flask-JWT-Extended
*   **Database Migrations:** Flask-Migrate (Alembic)
