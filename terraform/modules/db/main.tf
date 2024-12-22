terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = "d33b95c7-af3c-4247-9661-aa96d47fccc0"
}

data "azurerm_resource_group" "main" {
  name = "cohort32-33_TraWoo_ProjectExercise"
}

resource "azurerm_cosmosdb_account" "db" {
  name                 = "${var.prefix}-another-todo-app-cosmos-account"
  location             = data.azurerm_resource_group.main.location
  resource_group_name  = data.azurerm_resource_group.main.name
  offer_type           = "Standard"
  kind                 = "MongoDB"
  mongo_server_version = "4.2"
  ip_range_filter      = var.ip_ranges

  capabilities {
    name = "EnableServerless"
  }

  capabilities {
    name = "EnableMongo"
  }

  #  lifecycle {
  #    prevent_destroy = true
  #  }

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }

  geo_location {
    location          = "uksouth"
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_mongo_database" "db" {
  name                = "${var.prefix}-another_todoapp_db"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.db.name
}