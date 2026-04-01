provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name    = "terrakube-vpc"
    Project = "TerraKube-SelfHealOps"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true

  tags = {
    Name    = "terrakube-public-subnet"
    Project = "TerraKube-SelfHealOps"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name    = "terrakube-igw"
    Project = "TerraKube-SelfHealOps"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "terrakube-route-table"
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}


resource "aws_security_group" "terrakube_sg" {
  name        = "terrakube-sg"
  description = "Security group for TerraKube SelfHealOps"
  vpc_id      = aws_vpc.main.id


  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  
  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  
  ingress {
    from_port   = 6443
    to_port     = 6443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  
  ingress {
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  
  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "terrakube-sg"
    Project = "TerraKube-SelfHealOps"
  }
}

resource "aws_instance" "terrakube" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.terrakube_sg.id]
  key_name               = var.key_name

  root_block_device {
    volume_size = 20
    volume_type = "gp2"
  }

  user_data = <<-EOF
    #!/bin/bash
    apt-get update -y
    apt-get install -y docker.io curl
    systemctl start docker
    systemctl enable docker
    usermod -aG docker ubuntu
    docker pull ${var.dockerhub_username}/terrakube-selfhealops:latest
    docker run -d -p 5000:5000 --name terrakube-app ${var.dockerhub_username}/terrakube-selfhealops:latest
    curl -LO "https://dl.k8s.io/release/$(curl -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    chmod +x kubectl
    mv kubectl /usr/local/bin/
  EOF

  tags = {
    Name    = "terrakube-selfhealops"
    Project = "TerraKube-SelfHealOps"
  }
}
<<<<<<< HEAD
resource "aws_eip" "terrakube_eip" {
  instance = aws_instance.terrakube.id
  domain   = "vpc"

  tags = {
    Name    = "terrakube-eip"
    Project = "TerraKube-SelfHealOps"
  }
}
=======
>>>>>>> 86dbd14b103ea72c80e6350b65b603dae6d4f152
