output "ec2_public_dns" {
  description = "Public DNS of the EC2 instance"
  value       = aws_instance.terrakube.public_dns
}

output "ec2_public_ip" {
  description = "Static Elastic IP address"
  value       = aws_eip.terrakube_eip.public_ip
}

output "flask_app_url" {
  description = "Permanent URL for Flask dashboard"
  value       = "http://${aws_eip.terrakube_eip.public_ip}:5000"
}

output "ssh_command" {
  description = "SSH command to connect"
  value       = "ssh -i terrakube-key.pem ubuntu@${aws_eip.terrakube_eip.public_ip}"
}