output "ec2_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.terrakube.public_ip
}

output "ec2_public_dns" {
  description = "Public DNS of the EC2 instance"
  value       = aws_instance.terrakube.public_dns
}

output "flask_app_url" {
  description = "URL to access the Flask monitoring dashboard"
  value       = "http://${aws_instance.terrakube.public_ip}:5000"
}

output "ssh_command" {
  description = "SSH command to connect to your EC2 instance"
  value       = "ssh -i ${var.key_name}.pem ubuntu@${aws_instance.terrakube.public_ip}"
}
