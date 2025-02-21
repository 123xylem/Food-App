#  Menu Filter App

## Overview

This project implements a menu filtering system with pagination and real-time price calculations. Users can filter menus by cuisine and calculate total prices based on guest count.

## Tech Stack

- Frontend: React + TypeScript + TanStack Query
- Backend: Python Flask + SQLAlchemy
- Database: SQLite (for simplicty)

## Key Features

- Menu filtering by cuisine
- Real-time price calculations
- Infinite scroll pagination
- Cuisine aggregation stats
- Responsive design

## Challanges Faced

1. **Data Modeling**

   - Many-to-many relationships between menus and cusines
   - Needed proper indexing for performence
   - Aggregating order counts across cuisins

2. **API Design**

   - Implementing proper pagination
   - Handling rate limits for data harvsting
   - Optimizing query performance

3. **Frontend State**

   - Managing pagination state with React Query
   - Implementing infinite scroll
   - Calculating prices with minimum spend


## Improvements Needed

- Implement REDIS caching stratgy
- Improve test coverage
