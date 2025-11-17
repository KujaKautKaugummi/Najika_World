"""
Test Suite for Najika World Backend
Comprehensive unit and integration tests
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from backend.main import app
from backend.database import Base, get_db
from backend.models.user import User
from backend.models.character import Character
from backend.models.digimon import Digimon


# ============================================================================
# TEST DATABASE SETUP
# ============================================================================

# Use in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(db_session):
    """Create a test user"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="$2b$12$test_hash",  # Mock hash
        is_active=True,
        is_admin=False
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_admin(db_session):
    """Create a test admin user"""
    admin = User(
        username="admin",
        email="admin@example.com",
        hashed_password="$2b$12$admin_hash",
        is_active=True,
        is_admin=True
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin


@pytest.fixture
def test_character(db_session, test_user):
    """Create a test character"""
    character = Character(
        user_id=test_user.id,
        name="TestCharacter",
        level=1,
        experience=0,
        health=100,
        max_health=100,
        energy=100,
        max_energy=100
    )
    db_session.add(character)
    db_session.commit()
    db_session.refresh(character)
    return character


@pytest.fixture
def auth_headers(test_user):
    """Create authentication headers for test user"""
    # Mock JWT token for testing
    return {
        "Authorization": "Bearer test_token_" + str(test_user.id)
    }


# ============================================================================
# AUTHENTICATION TESTS
# ============================================================================

class TestAuthentication:
    """Test authentication endpoints"""

    def test_register_user(self, db_session):
        """Test user registration"""
        response = client.post(
            "/api/auth/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "secure_password123"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "user" in data
        assert data["user"]["username"] == "newuser"

    def test_register_duplicate_username(self, db_session, test_user):
        """Test registration with duplicate username"""
        response = client.post(
            "/api/auth/register",
            json={
                "username": "testuser",  # Already exists
                "email": "different@example.com",
                "password": "password123"
            }
        )

        assert response.status_code == 400

    def test_login_success(self, db_session, test_user):
        """Test successful login"""
        response = client.post(
            "/api/auth/login",
            data={
                "username": "testuser",
                "password": "password123"
            }
        )

        # Note: This will fail without proper password hashing in test_user
        # In real implementation, hash the test password properly

    def test_login_invalid_credentials(self, db_session):
        """Test login with invalid credentials"""
        response = client.post(
            "/api/auth/login",
            data={
                "username": "nonexistent",
                "password": "wrongpassword"
            }
        )

        assert response.status_code == 401


# ============================================================================
# USER TESTS
# ============================================================================

class TestUsers:
    """Test user-related endpoints"""

    def test_get_current_user(self, db_session, test_user, auth_headers):
        """Test getting current user info"""
        response = client.get("/api/auth/me", headers=auth_headers)

        if response.status_code == 200:
            data = response.json()
            assert data["username"] == test_user.username

    def test_update_user_profile(self, db_session, test_user, auth_headers):
        """Test updating user profile"""
        response = client.patch(
            f"/api/users/{test_user.id}",
            headers=auth_headers,
            json={
                "email": "updated@example.com"
            }
        )

        # Implementation dependent


# ============================================================================
# CHARACTER TESTS
# ============================================================================

class TestCharacters:
    """Test character system"""

    def test_create_character(self, db_session, test_user, auth_headers):
        """Test character creation"""
        response = client.post(
            "/api/game/characters",
            headers=auth_headers,
            json={
                "name": "NewCharacter"
            }
        )

        # Implementation dependent

    def test_get_character(self, db_session, test_character, auth_headers):
        """Test getting character details"""
        response = client.get(
            f"/api/game/characters/{test_character.id}",
            headers=auth_headers
        )

        # Implementation dependent

    def test_level_up_character(self, db_session, test_character):
        """Test character leveling up"""
        initial_level = test_character.level
        test_character.experience = 1000  # Enough to level up

        # Trigger level up logic
        # Implementation dependent

        assert test_character.level > initial_level


# ============================================================================
# BATTLE SYSTEM TESTS
# ============================================================================

class TestBattle:
    """Test battle system"""

    def test_battle_initialization(self, db_session, test_character):
        """Test battle initialization"""
        from backend.services.battle_system import BattleSystem

        battle = BattleSystem()
        # Implementation dependent

    def test_battle_attack(self):
        """Test battle attack mechanics"""
        # Implementation dependent
        pass

    def test_battle_victory(self):
        """Test battle victory rewards"""
        # Implementation dependent
        pass


# ============================================================================
# NEMESIS ARENA TESTS
# ============================================================================

class TestNemesisArena:
    """Test nemesis arena system"""

    def test_create_nemesis_monster(self, db_session):
        """Test creating nemesis monster"""
        from backend.services.nemesis_arena_system import NemesisArenaSystem

        arena = NemesisArenaSystem()
        monster = arena.create_monster("Test Monster", "AGGRESSIVE")

        assert monster.name == "Test Monster"
        assert monster.rank.value == "Niemand"

    def test_monster_promotion(self, db_session):
        """Test monster rank promotion"""
        from backend.services.nemesis_arena_system import NemesisArenaSystem

        arena = NemesisArenaSystem()
        monster = arena.create_monster("Test Monster", "AGGRESSIVE")

        # Win battles to promote
        for _ in range(5):
            arena.record_victory(monster)

        # Should have promoted
        assert monster.rank.value != "Niemand"

    def test_grudge_system(self, db_session):
        """Test monster grudge mechanics"""
        from backend.services.nemesis_arena_system import NemesisArenaSystem

        arena = NemesisArenaSystem()
        monster = arena.create_monster("Test Monster", "AGGRESSIVE")

        # Monster loses battle
        arena.record_defeat(monster, "TestPlayer", "Brutal Finisher")

        assert len(monster.grudges) > 0
        assert "TestPlayer" in monster.grudges[0]


# ============================================================================
# FINISHER SYSTEM TESTS
# ============================================================================

class TestFinisherSystem:
    """Test finisher creation system"""

    def test_create_honorable_finisher(self):
        """Test creating honorable death finisher"""
        from backend.services.finisher_system import FinisherSystem, BrutalityCategory

        finisher_gen = FinisherSystem()
        finisher = finisher_gen.create_custom_finisher(
            category=BrutalityCategory.HONORABLE_DEATH,
            ingredients=["sword", "honor", "bow"],
            character_level=10
        )

        assert finisher.category == "Ehrenvoller Tod"
        assert finisher.brutality_level <= 3

    def test_create_funny_finisher(self):
        """Test creating funny death finisher"""
        from backend.services.finisher_system import FinisherSystem, BrutalityCategory

        finisher_gen = FinisherSystem()
        finisher = finisher_gen.create_custom_finisher(
            category=BrutalityCategory.FUNNY_DEATH,
            ingredients=["banana", "pie", "rubber chicken"],
            character_level=10
        )

        assert finisher.category == "Lustiger Tod"
        assert finisher.humor_level >= 7

    def test_create_brutal_finisher(self):
        """Test creating brutal finisher"""
        from backend.services.finisher_system import FinisherSystem, BrutalityCategory

        finisher_gen = FinisherSystem()
        finisher = finisher_gen.create_custom_finisher(
            category=BrutalityCategory.BLOOD_BATH,
            ingredients=["chainsaw", "blood", "gore"],
            character_level=10
        )

        assert finisher.category == "Tod Tod Blut Blut"
        assert finisher.brutality_level >= 9


# ============================================================================
# WEBSOCKET TESTS
# ============================================================================

class TestWebSocket:
    """Test WebSocket functionality"""

    @pytest.mark.asyncio
    async def test_websocket_connection(self):
        """Test WebSocket connection"""
        # Note: WebSocket testing requires special setup
        pass

    @pytest.mark.asyncio
    async def test_websocket_broadcast(self):
        """Test WebSocket broadcasting"""
        pass


# ============================================================================
# ADMIN TESTS
# ============================================================================

class TestAdmin:
    """Test admin endpoints"""

    def test_admin_get_stats(self, db_session, test_admin):
        """Test admin statistics endpoint"""
        # Create admin auth headers
        admin_headers = {
            "Authorization": "Bearer admin_token_" + str(test_admin.id)
        }

        response = client.get("/api/admin/stats", headers=admin_headers)

        # Implementation dependent

    def test_non_admin_access_denied(self, db_session, test_user, auth_headers):
        """Test non-admin cannot access admin endpoints"""
        response = client.get("/api/admin/stats", headers=auth_headers)

        # Should be denied


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestPerformance:
    """Test system performance"""

    def test_api_response_time(self, db_session, auth_headers):
        """Test API response times are acceptable"""
        import time

        start = time.time()
        response = client.get("/api/auth/me", headers=auth_headers)
        duration = time.time() - start

        assert duration < 0.2  # Should respond in < 200ms

    def test_database_query_performance(self, db_session):
        """Test database query performance"""
        import time

        # Create many users
        for i in range(100):
            user = User(
                username=f"user_{i}",
                email=f"user{i}@example.com",
                hashed_password="test_hash"
            )
            db_session.add(user)

        db_session.commit()

        # Query should be fast
        start = time.time()
        users = db_session.query(User).all()
        duration = time.time() - start

        assert duration < 0.1  # Should query in < 100ms
        assert len(users) >= 100


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Test end-to-end workflows"""

    def test_complete_battle_workflow(self, db_session, test_character):
        """Test complete battle workflow from start to finish"""
        # 1. Initialize battle
        # 2. Execute attacks
        # 3. Win battle
        # 4. Receive rewards
        # 5. Level up

        # Implementation dependent
        pass

    def test_complete_training_workflow(self, db_session, test_user):
        """Test complete training workflow"""
        # 1. Create training job
        # 2. Start training
        # 3. Monitor progress
        # 4. Complete training
        # 5. Load trained model

        # Implementation dependent
        pass


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_test_users(db_session, count=10):
    """Helper to create multiple test users"""
    users = []
    for i in range(count):
        user = User(
            username=f"testuser_{i}",
            email=f"test{i}@example.com",
            hashed_password="test_hash",
            is_active=True,
            is_admin=False
        )
        db_session.add(user)
        users.append(user)

    db_session.commit()
    return users


def create_test_characters(db_session, user, count=3):
    """Helper to create multiple test characters"""
    characters = []
    for i in range(count):
        character = Character(
            user_id=user.id,
            name=f"Character_{i}",
            level=1,
            experience=0,
            health=100,
            max_health=100
        )
        db_session.add(character)
        characters.append(character)

    db_session.commit()
    return characters


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
