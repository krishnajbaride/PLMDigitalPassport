"""
Phase v1.0 - Connector Framework for ERP/MES Integration
Pluggable connector architecture for enterprise systems
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from enum import Enum
import logging


class ConnectorType(str, Enum):
    """Types of enterprise systems"""
    ERP = "erp"
    MES = "mes"
    DOCUMENT = "document"
    IDENTITY = "identity"


class ConnectorStatus(str, Enum):
    """Connector status"""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    INITIALIZING = "initializing"


class BaseConnector(ABC):
    """
    Abstract base class for all enterprise connectors
    Defines the interface that all connector implementations must follow
    """
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.status = ConnectorStatus.DISCONNECTED
        self.logger = logging.getLogger(f"connector.{name}")
        self._metadata = {}
    
    @abstractmethod
    def connect(self) -> bool:
        """
        Establish connection to the enterprise system
        
        Returns:
            True if connection successful, False otherwise
        """
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """
        Close connection to the enterprise system
        
        Returns:
            True if disconnection successful, False otherwise
        """
        pass
    
    @abstractmethod
    def test_connection(self) -> tuple[bool, str]:
        """
        Test if connection is working
        
        Returns:
            Tuple of (is_connected, message)
        """
        pass
    
    @abstractmethod
    def get_parts(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Fetch parts from enterprise system
        
        Args:
            filters: Optional filters for querying
            
        Returns:
            List of part records
        """
        pass
    
    @abstractmethod
    def get_bom(self, product_id: str) -> Dict[str, Any]:
        """
        Fetch BOM for a product
        
        Args:
            product_id: Product identifier in the source system
            
        Returns:
            BOM data
        """
        pass
    
    @abstractmethod
    def create_part(self, part_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create part in enterprise system
        
        Args:
            part_data: Part information
            
        Returns:
            Created part record with system ID
        """
        pass
    
    @abstractmethod
    def update_part(self, part_id: str, part_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update part in enterprise system
        
        Args:
            part_id: Part ID in source system
            part_data: Updated part information
            
        Returns:
            Updated part record
        """
        pass
    
    @abstractmethod
    def sync_bom(self, product_id: str, bom_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sync BOM changes to enterprise system
        
        Args:
            product_id: Product identifier
            bom_data: BOM data to sync
            
        Returns:
            Sync result with status and affected records
        """
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get connector status"""
        return {
            "name": self.name,
            "status": self.status.value,
            "metadata": self._metadata
        }
    
    def log_operation(self, operation: str, details: Dict[str, Any]) -> None:
        """Log connector operation for audit trail"""
        self.logger.info(f"{operation}: {details}")


class ERPConnector(BaseConnector):
    """Base class for ERP system connectors"""
    
    connector_type = ConnectorType.ERP
    
    @abstractmethod
    def get_purchase_orders(self) -> List[Dict[str, Any]]:
        """Fetch purchase orders"""
        pass
    
    @abstractmethod
    def get_supplier_data(self, supplier_id: str) -> Dict[str, Any]:
        """Fetch supplier information"""
        pass
    
    @abstractmethod
    def sync_inventory(self, inventory_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Sync inventory data"""
        pass


class MESConnector(BaseConnector):
    """Base class for MES system connectors"""
    
    connector_type = ConnectorType.MES
    
    @abstractmethod
    def get_production_orders(self) -> List[Dict[str, Any]]:
        """Fetch production orders"""
        pass
    
    @abstractmethod
    def get_work_orders(self, filter_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetch work orders"""
        pass
    
    @abstractmethod
    def report_production(self, production_data: Dict[str, Any]) -> bool:
        """Report production completed"""
        pass


class ConnectorRegistry:
    """
    Registry for managing connector instances
    Implements factory pattern for connector creation
    """
    
    def __init__(self):
        self._connectors: Dict[str, BaseConnector] = {}
        self._registry: Dict[str, type] = {}
    
    def register(self, system_name: str, connector_class: type) -> None:
        """
        Register a connector class
        
        Args:
            system_name: System identifier (e.g., 'sap', 'oracle')
            connector_class: Connector class that extends BaseConnector
        """
        if not issubclass(connector_class, BaseConnector):
            raise ValueError(f"{connector_class} must be subclass of BaseConnector")
        
        self._registry[system_name] = connector_class
    
    def create_connector(self, 
                        system_name: str,
                        instance_name: str,
                        config: Dict[str, Any]) -> BaseConnector:
        """
        Create and register connector instance
        
        Args:
            system_name: System type (must be registered)
            instance_name: Unique instance name
            config: Configuration for the connector
            
        Returns:
            Connector instance
        """
        if system_name not in self._registry:
            raise ValueError(f"Connector for {system_name} not registered")
        
        connector_class = self._registry[system_name]
        connector = connector_class(instance_name, config)
        self._connectors[instance_name] = connector
        
        return connector
    
    def get_connector(self, instance_name: str) -> Optional[BaseConnector]:
        """Get connector by instance name"""
        return self._connectors.get(instance_name)
    
    def list_connectors(self) -> Dict[str, Dict[str, Any]]:
        """List all active connectors with their status"""
        return {
            name: connector.get_status()
            for name, connector in self._connectors.items()
        }
    
    def disconnect_all(self) -> None:
        """Disconnect all active connectors"""
        for connector in self._connectors.values():
            try:
                connector.disconnect()
            except Exception as e:
                logging.error(f"Error disconnecting {connector.name}: {e}")


# Example connector implementations
class MockSAPConnector(ERPConnector):
    """Mock SAP connector for testing"""
    
    def connect(self) -> bool:
        self.status = ConnectorStatus.CONNECTED
        self._metadata['system_id'] = 'SAP_DEV'
        return True
    
    def disconnect(self) -> bool:
        self.status = ConnectorStatus.DISCONNECTED
        return True
    
    def test_connection(self) -> tuple[bool, str]:
        if self.status == ConnectorStatus.CONNECTED:
            return True, "Connected to SAP successfully"
        return False, "Not connected to SAP"
    
    def get_parts(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        return [
            {"part_number": "SAP001", "description": "Part from SAP"},
            {"part_number": "SAP002", "description": "Another SAP part"}
        ]
    
    def get_bom(self, product_id: str) -> Dict[str, Any]:
        return {"product_id": product_id, "parts": []}
    
    def create_part(self, part_data: Dict[str, Any]) -> Dict[str, Any]:
        return {**part_data, "sap_id": "NEW_SAP_ID"}
    
    def update_part(self, part_id: str, part_data: Dict[str, Any]) -> Dict[str, Any]:
        return {**part_data, "sap_id": part_id}
    
    def sync_bom(self, product_id: str, bom_data: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "synced", "product_id": product_id}
    
    def get_purchase_orders(self) -> List[Dict[str, Any]]:
        return []
    
    def get_supplier_data(self, supplier_id: str) -> Dict[str, Any]:
        return {"supplier_id": supplier_id}
    
    def sync_inventory(self, inventory_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {"status": "synced", "records": len(inventory_data)}
