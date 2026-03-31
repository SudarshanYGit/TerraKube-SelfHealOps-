variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "ap-south-1"
}

variable "ami_id" {
  description = "Ubuntu 22.04 AMI ID for ap-south-1 (Mumbai)"
  type        = string
  default     = "ami-05d2d839d4f73aafb"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "Name of your AWS key pair for SSH access"
  type        = string
  default     = "terrakube-key"
}

variable "dockerhub_username" {
  description = "Your Docker Hub username"
  type        = string
  default     = "sudarshan72docker"
}
