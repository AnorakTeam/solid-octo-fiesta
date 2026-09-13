# ==============================================================================
# Red y Subred VPC Dedicada
# ==============================================================================
resource "google_compute_network" "vpc_network" {
  name                    = "${var.app_name}-${var.environment}-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet" {
  name          = "${var.app_name}-${var.environment}-subnet"
  ip_cidr_range = "10.10.1.0/24"
  region        = var.gcp_region
  network       = google_compute_network.vpc_network.id
}

# ==============================================================================
# IP Externa Estática Pública (Sin Dominio)
# ==============================================================================
resource "google_compute_address" "static_ip" {
  name        = "${var.app_name}-${var.environment}-public-ip"
  region      = var.gcp_region
  description = "IP publica estática para el despliegue de microservicios"
}

# ==============================================================================
# Reglas de Firewall
# ==============================================================================
# 1. Permitir SSH (Puerto 22)
resource "google_compute_firewall" "allow_ssh" {
  name    = "${var.app_name}-${var.environment}-allow-ssh"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = var.allowed_ingress_cidrs
  target_tags   = ["solid-octo-server"]
}

# 2. Permitir Tráfico Web (HTTP 80, HTTPS 443, Frontend 3000, Gateway 8000) e ICMP (Ping)
resource "google_compute_firewall" "allow_web" {
  name    = "${var.app_name}-${var.environment}-allow-web"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["80", "443", "3000", "8000"]
  }

  allow {
    protocol = "icmp"
  }

  source_ranges = var.allowed_ingress_cidrs
  target_tags   = ["solid-octo-server"]
}

# ==============================================================================
# Cuenta de Servicio para la VM (Principle of Least Privilege)
# ==============================================================================
resource "google_service_account" "vm_sa" {
  account_id   = "${var.app_name}-${var.environment}-vm-sa"
  display_name = "Service Account para VM de ${var.app_name}"
}

# ==============================================================================
# Instancia de Compute Engine (VM de Bajo Costo)
# ==============================================================================
resource "google_compute_instance" "app_vm" {
  name         = "${var.app_name}-${var.environment}-vm"
  machine_type = var.machine_type
  zone         = var.gcp_zone

  tags = ["solid-octo-server"]

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
      size  = var.boot_disk_size_gb
      type  = var.boot_disk_type
    }
  }

  network_interface {
    network    = google_compute_network.vpc_network.name
    subnetwork = google_compute_subnetwork.subnet.name

    access_config {
      nat_ip = google_compute_address.static_ip.address
    }
  }

  metadata_startup_script = file("${path.module}/scripts/startup.sh")

  metadata = {
    ssh-keys = var.ssh_public_key != "" ? "${var.ssh_user}:${var.ssh_public_key}" : null
  }

  service_account {
    email  = google_service_account.vm_sa.email
    scopes = ["cloud-platform"]
  }

  shielded_instance_config {
    enable_secure_boot          = true
    enable_vtpm                 = true
    enable_integrity_monitoring = true
  }

  labels = {
    environment = var.environment
    managed_by  = "terraform"
    app         = var.app_name
  }
}
