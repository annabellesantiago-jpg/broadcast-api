# Testing Guide

## Backend Testing

### Unit Tests

Create `backend/tests/test_auth.py`:

```python
import unittest
from app import create_app, db
from app.models import User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_signup_success(self):
        response = self.client.post('/api/auth/signup', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('access_token', response.json)
    
    def test_signup_duplicate_username(self):
        self.client.post('/api/auth/signup', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        })
        response = self.client.post('/api/auth/signup', json={
            'username': 'testuser',
            'email': 'test2@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 409)
    
    def test_login_success(self):
        self.client.post('/api/auth/signup', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        })
        response = self.client.post('/api/auth/login', json={
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)
    
    def test_login_invalid_credentials(self):
        response = self.client.post('/api/auth/login', json={
            'username': 'nonexistent',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
```

### Run Tests

```bash
cd backend
python -m pytest tests/ -v

# Or with unittest
python -m unittest discover
```

## Frontend Testing

### Component Tests with Jest

Create `frontend/src/components/__tests__/Login.test.js`:

```javascript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Login from '../Login';

describe('Login Component', () => {
  test('renders login form', () => {
    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );
    expect(screen.getByPlaceholderText('Username')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Password')).toBeInTheDocument();
  });

  test('submits login form', async () => {
    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );
    
    fireEvent.change(screen.getByPlaceholderText('Username'), {
      target: { value: 'testuser' },
    });
    fireEvent.change(screen.getByPlaceholderText('Password'), {
      target: { value: 'testpass' },
    });
    fireEvent.click(screen.getByText('Login'));

    await waitFor(() => {
      expect(screen.getByText('Logging in...')).toBeInTheDocument();
    });
  });
});
```

### Run Tests

```bash
cd frontend
npm test
```

## Mobile Testing

### Widget Tests

Create `mobile/test/widgets/login_test.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:broadcast_management_mobile/screens/login_screen.dart';

void main() {
  group('Login Screen', () {
    testWidgets('renders login form', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(home: LoginScreen()),
      );

      expect(find.byType(TextField), findsWidgets);
      expect(find.byType(ElevatedButton), findsOneWidget);
      expect(find.text('Login'), findsOneWidget);
    });

    testWidgets('shows error on invalid login', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(home: LoginScreen()),
      );

      await tester.enterText(find.byType(TextField).first, 'testuser');
      await tester.enterText(find.byType(TextField).last, 'wrongpass');
      await tester.tap(find.byType(ElevatedButton));
      await tester.pump();

      expect(find.byType(Text), findsWidgets);
    });
  });
}
```

### Run Tests

```bash
cd mobile
flutter test
```

## Integration Tests

### Backend + Database

```python
# backend/tests/test_broadcasts.py
def test_broadcast_workflow(self):
    # 1. Create user
    signup_response = self.client.post('/api/auth/signup', json={...})
    token = signup_response.json['access_token']
    
    # 2. Create broadcast
    broadcast_response = self.client.post(
        '/api/broadcasts',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Test', 'message': 'Test message'}
    )
    self.assertEqual(broadcast_response.status_code, 201)
    
    # 3. Send broadcast
    broadcast_id = broadcast_response.json['broadcast']['id']
    send_response = self.client.post(
        f'/api/broadcasts/{broadcast_id}/send',
        headers={'Authorization': f'Bearer {token}'},
        json={}
    )
    self.assertEqual(send_response.status_code, 200)
```

## Load Testing

### Using Apache Bench

```bash
# Test API endpoint
ab -n 1000 -c 100 http://localhost:5000/api/broadcasts

# With authentication header
ab -n 1000 -c 100 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/api/broadcasts
```

### Using Locust

Create `backend/locustfile.py`:

```python
from locust import HttpUser, task, between

class BroadcastUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def list_broadcasts(self):
        self.client.get(
            "/api/broadcasts",
            headers={"Authorization": "Bearer token"}
        )
    
    @task
    def create_broadcast(self):
        self.client.post(
            "/api/broadcasts",
            headers={"Authorization": "Bearer token"},
            json={
                "title": "Test",
                "message": "Test message"
            }
        )
```

Run: `locust -f backend/locustfile.py`

## End-to-End Testing (Selenium)

```python
# frontend/e2e/test_broadcast_flow.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_broadcast_creation():
    driver = webdriver.Chrome()
    driver.get("http://localhost:3000")
    
    # Login
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    
    username_input.send_keys("testuser")
    password_input.send_keys("testpass")
    
    login_button = driver.find_element(By.XPATH, "//button[text()='Login']")
    login_button.click()
    
    # Wait for dashboard
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TEXT, "Create New Broadcast"))
    )
    
    # Create broadcast
    create_button = driver.find_element(By.TEXT, "Create New Broadcast")
    create_button.click()
    
    driver.quit()
```

## Test Coverage

### Generate Coverage Report

**Backend:**
```bash
cd backend
pip install coverage
coverage run -m pytest tests/
coverage report
coverage html  # Generates htmlcov/index.html
```

**Frontend:**
```bash
cd frontend
npm test -- --coverage
```

## Continuous Testing

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: admin
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - run: pip install -r backend/requirements.txt
      - run: cd backend && python -m pytest

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: 16
      - run: cd frontend && npm install && npm test
```

## Test Checklist

- [ ] Unit tests for backend models
- [ ] API endpoint tests
- [ ] Authentication tests
- [ ] Component tests for frontend
- [ ] Integration tests
- [ ] E2E tests for critical flows
- [ ] Load testing
- [ ] Security testing
- [ ] Cross-browser testing
- [ ] Mobile device testing

## Performance Testing

Check response times and identify bottlenecks:

```bash
# Backend performance
python -m cProfile -s cumulative backend/app.py

# Frontend performance (Chrome DevTools)
# Frontend > Performance tab
```
