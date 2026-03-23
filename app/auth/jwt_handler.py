"""
Phase v0.4 - Authentication & Authorization Module
JWT-based authentication and role-based access control
"""

from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import HTTPException, status
import jwt
from passlib.context import CryptContext
from enum import Enum


class UserRole(str, Enum):
    """User roles for RBAC"""
    ADMIN = "admin"
    ENGINEER = "engineer"
    VIEWER = "viewer"
    SUPPLIER = "supplier"


class Permission(str, Enum):
    """Permissions for role-based access"""
    # Part management
    CREATE_PART = "create_part"
    READ_PART = "read_part"
    UPDATE_PART = "update_part"
    DELETE_PART = "delete_part"
    
    # BOM management
    CREATE_BOM = "create_bom"
    READ_BOM = "read_bom"
    UPDATE_BOM = "update_bom"
    DELETE_BOM = "delete_bom"
    
    # ECO/Change management
    CREATE_ECO = "create_eco"
    READ_ECO = "read_eco"
    UPDATE_ECO = "update_eco"
    DELETE_ECO = "delete_eco"
    APPROVE_ECO = "approve_eco"
    
    # Import/Export
    IMPORT_BOM = "import_bom"
    EXPORT_DATA = "export_data"
    
    # User management
    MANAGE_USERS = "manage_users"
    MANAGE_ROLES = "manage_roles"
    
    # Audit
    VIEW_AUDIT_LOG = "view_audit_log"


class JWTHandler:
    """Handle JWT token creation and validation"""
    
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def create_token(self, 
                    user_id: str, 
                    username: str, 
                    roles: List[str],
                    expires_in_hours: int = 24) -> str:
        """Create JWT token"""
        expire = datetime.utcnow() + timedelta(hours=expires_in_hours)
        
        payload = {
            "user_id": user_id,
            "username": username,
            "roles": roles,
            "exp": expire,
            "iat": datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    def verify_token(self, token: str) -> dict:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    
    def hash_password(self, password: str) -> str:
        """Hash password for storage"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return self.pwd_context.verify(plain_password, hashed_password)


class RBACManager:
    """Manage role-based access control"""
    
    # Default permissions for each role
    ROLE_PERMISSIONS = {
        UserRole.ADMIN: [
            Permission.CREATE_PART, Permission.READ_PART, Permission.UPDATE_PART, Permission.DELETE_PART,
            Permission.CREATE_BOM, Permission.READ_BOM, Permission.UPDATE_BOM, Permission.DELETE_BOM,
            Permission.CREATE_ECO, Permission.READ_ECO, Permission.UPDATE_ECO, Permission.DELETE_ECO, Permission.APPROVE_ECO,
            Permission.IMPORT_BOM, Permission.EXPORT_DATA,
            Permission.MANAGE_USERS, Permission.MANAGE_ROLES,
            Permission.VIEW_AUDIT_LOG
        ],
        UserRole.ENGINEER: [
            Permission.CREATE_PART, Permission.READ_PART, Permission.UPDATE_PART,
            Permission.CREATE_BOM, Permission.READ_BOM, Permission.UPDATE_BOM,
            Permission.CREATE_ECO, Permission.READ_ECO, Permission.UPDATE_ECO,
            Permission.IMPORT_BOM, Permission.EXPORT_DATA,
            Permission.VIEW_AUDIT_LOG
        ],
        UserRole.VIEWER: [
            Permission.READ_PART,
            Permission.READ_BOM,
            Permission.READ_ECO,
            Permission.EXPORT_DATA,
            Permission.VIEW_AUDIT_LOG
        ],
        UserRole.SUPPLIER: [
            Permission.READ_PART,
            Permission.VIEW_AUDIT_LOG
        ]
    }
    
    def has_permission(self, roles: List[str], permission: Permission) -> bool:
        """Check if any of the roles has the given permission"""
        for role in roles:
            try:
                user_role = UserRole(role)
                if permission in self.ROLE_PERMISSIONS.get(user_role, []):
                    return True
            except ValueError:
                continue
        return False
    
    def check_permission(self, roles: List[str], permission: Permission) -> None:
        """Raise exception if permission not granted"""
        if not self.has_permission(roles, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: {permission.value} required"
            )


# Usage example for FastAPI
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthCredentials

app = FastAPI()
security = HTTPBearer()
jwt_handler = JWTHandler(secret_key="your-secret-key")
rbac = RBACManager()

async def get_current_user(credentials: HTTPAuthCredentials = Depends(security)):
    token = credentials.credentials
    return jwt_handler.verify_token(token)

async def require_permission(permission: Permission):
    async def check_perm(current_user: dict = Depends(get_current_user)):
        rbac.check_permission(current_user["roles"], permission)
        return current_user
    return check_perm

@app.post("/api/v1/boms")
async def create_bom(bom_data: dict, current_user: dict = Depends(require_permission(Permission.CREATE_BOM))):
    # Audit log
    print(f"User {current_user['username']} created BOM")
    return {"status": "created", "user": current_user["username"]}
"""
