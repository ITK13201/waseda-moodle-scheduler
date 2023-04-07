# Terraform

## terraform commands

### init

```shell
terraform init -backend-config=./backend.conf
```

### plan

```shell
terraform plan -var-file=./terraform.tfvars
```

### apply

```shell
terraform apply -var-file=./terraform.tfvars
```

## GCP

### init

```shell
gcloud init
```

### Application Default Credentials (ADC)

```shell
gcloud auth application-default login
```
