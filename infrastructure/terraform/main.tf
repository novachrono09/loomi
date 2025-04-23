terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "loomi_vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = {
    Name = "loomi-vpc"
  }
}

resource "aws_subnet" "loomi_public_subnet" {
  vpc_id     = aws_vpc.loomi_vpc.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "us-east-1a"
  map_public_ip_on_launch = true
  tags = {
    Name = "loomi-public-subnet"
  }
}

resource "aws_internet_gateway" "loomi_igw" {
  vpc_id = aws_vpc.loomi_vpc.id
  tags = {
    Name = "loomi-igw"
  }
}

resource "aws_route_table" "loomi_public_rt" {
  vpc_id = aws_vpc.loomi_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.loomi_igw.id
  }
  tags = {
    Name = "loomi-public-rt"
  }
}

resource "aws_route_table_association" "loomi_public_rta" {
  subnet_id      = aws_subnet.loomi_public_subnet.id
  route_table_id = aws_route_table.loomi_public_rt.id
}

resource "aws_security_group" "loomi_sg" {
  name        = "loomi-sg"
  description = "Allow all necessary traffic for Loomi"
  vpc_id      = aws_vpc.loomi_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 4000
    to_port     = 4000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5000
    to_port     = 5002
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
    Name = "loomi-sg"
  }
}

resource "aws_ecs_cluster" "loomi_cluster" {
  name = "loomi-cluster"
}

resource "aws_ecs_task_definition" "loomi_task" {
  family                   = "loomi-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "1024"
  memory                   = "2048"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "frontend"
      image     = "loomi-frontend:latest"
      cpu       = 256
      memory    = 512
      essential = true
      portMappings = [
        {
          containerPort = 3000
          hostPort      = 3000
        }
      ]
    },
    {
      name      = "backend"
      image     = "loomi-backend:latest"
      cpu       = 512
      memory    = 1024
      essential = true
      portMappings = [
        {
          containerPort = 4000
          hostPort      = 4000
        }
      ]
    },
    {
      name      = "ai-orchestrator"
      image     = "loomi-ai-orchestrator:latest"
      cpu       = 512
      memory    = 1024
      essential = true
      portMappings = [
        {
          containerPort = 5000
          hostPort      = 5000
        }
      ]
    }
  ])
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "loomi-ecs-task-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_ecs_service" "loomi_service" {
  name            = "loomi-service"
  cluster         = aws_ecs_cluster.loomi_cluster.id
  task_definition = aws_ecs_task_definition.loomi_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = [aws_subnet.loomi_public_subnet.id]
    security_groups = [aws_security_group.loomi_sg.id]
    assign_public_ip = true
  }
}

output "frontend_url" {
  value = "http://${aws_ecs_service.loomi_service.load_balancer[0].dns_name}:3000"
}

output "backend_url" {
  value = "http://${aws_ecs_service.loomi_service.load_balancer[0].dns_name}:4000"
}