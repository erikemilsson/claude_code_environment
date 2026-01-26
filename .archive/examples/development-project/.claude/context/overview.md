# Project Overview

## Purpose

Build a REST API for todo item management with user authentication.

## Current State

Early development - setting up authentication and basic CRUD.

## Key Components

- **Auth Module**: JWT-based authentication with register/login
- **Todo Module**: CRUD operations for todo items
- **Database**: PostgreSQL with Prisma ORM

## Technical Decisions

- Using Express.js for simplicity (team is familiar)
- JWT tokens stored in httpOnly cookies (more secure than localStorage)
- Prisma ORM for type-safe database access

## Notes

- Need to implement rate limiting before production
- Consider adding refresh tokens in future iteration
