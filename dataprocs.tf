provider "google" {
  project     = "your-project-id"
  region      = "your-region"
}

resource "google_dataproc_cluster" "example_cluster" {
  name          = "my-dataprocs-$(date +'%Y%m%d%H%M%S')"
  project       = "your-project-id"
  region        = "your-region"
  cluster_config {
    master_config {
disk_config {
        boot_disk_size_gb = 50
      }
      num_instances = 1
      machine_type = "n1-standard-4"
    }

    worker_config {
disk_config {
        boot_disk_size_gb = 50
      }
      num_instances = 2
      machine_type = "n1-standard-4"
    }
  }
}
