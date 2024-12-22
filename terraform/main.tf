terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }

  backend "azurerm" {
    resource_group_name  = "cohort32-33_TraWoo_ProjectExercise"
    storage_account_name = "trawootfstate"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
  subscription_id = "d33b95c7-af3c-4247-9661-aa96d47fccc0"
}

data "azurerm_resource_group" "main" {
  name = "cohort32-33_TraWoo_ProjectExercise"
}

resource "azurerm_service_plan" "main" {
  name                = "${var.prefix}-another-todo-app"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "main" {
  name                = "${var.prefix}-travis-woodward-another-todo-app"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      docker_image_name   = "trwoodward/todo-app:latest"
      docker_registry_url = "https://index.docker.io"
    }
  }
  app_settings = {
    "FLASK_APP"                = "todo_app/app"
    "SECRET_KEY"               = var.secret_key
    "GITHUB_CLIENT_ID"         = var.github_client_id
    "GITHUB_CLIENT_SECRET"     = var.github_client_secret
    "COSMOS_CONNECTION_STRING" = module.db.cosmos_connection_string
  }
}

locals {
  portal_ips = [
    "13.91.105.215",
    "4.210.172.107",
    "13.88.56.148",
    "40.91.218.243",
    "20.245.81.54",
    "40.118.23.126",
    "40.80.152.199",
    "13.95.130.121"
  ]
  #  Must be added manually to avoid dependency cycle between app and cosmos account
  app_ips = [
    "4.159.115.45",
    "4.159.115.120",
    "4.159.115.122",
    "4.159.115.126",
    "4.159.115.128",
    "4.159.115.134",
    "4.159.113.137",
    "4.159.113.141",
    "4.159.113.148",
    "4.159.112.213",
    "4.159.113.211",
    "172.165.151.213",
    "4.250.136.242",
    "4.159.113.218",
    "4.159.113.243",
    "4.159.114.0",
    "4.159.114.15",
    "4.159.114.16",
    "172.165.149.246",
    "4.159.114.33",
    "4.159.114.34",
    "4.159.114.46",
    "4.159.114.72",
    "4.159.114.172",
    "4.159.115.137",
    "4.159.115.148",
    "4.159.115.163",
    "4.159.115.185",
    "4.159.114.132",
    "4.159.114.142",
    "20.90.134.37"
  ]
  all_ips = concat(local.portal_ips, local.app_ips)
}

module "db" {
  source = "./modules/db"

  prefix    = var.prefix
  ip_ranges = local.all_ips
}