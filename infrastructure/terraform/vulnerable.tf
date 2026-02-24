# infrastructure/terraform/vulnerable.tf
provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "vulnerable_bucket" {
  bucket = "vulnerable-public-bucket-example"
  acl    = "public-read"   # ⚠️ Esto hace que el bucket sea público/es para probar el agente
}

resource "aws_s3_bucket_policy" "public_policy" {
  bucket = aws_s3_bucket.vulnerable_bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = ["s3:GetObject"]
        Resource  = "${aws_s3_bucket.vulnerable_bucket.arn}/*"
      }
    ]
  })
}