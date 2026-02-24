provider "aws" {
  region = "us-east-1"
}

# Bucket totalmente público y vulnerable
resource "aws_s3_bucket" "super_vulnerable" {
  bucket = "super-vulnerable-bucket-example"
  acl    = "public-read-write"  # ⚠️ permite lectura y escritura a cualquier persona
  force_destroy = true           # ⚠️ permite borrar el bucket con objetos dentro
}

# Política pública que permite cualquier acción de S3
resource "aws_s3_bucket_policy" "public_policy" {
  bucket = aws_s3_bucket.super_vulnerable.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "FullPublicAccess"
        Effect    = "Allow"
        Principal = "*"
        Action    = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket",
          "s3:PutObjectAcl",
          "s3:GetBucketPolicy"
        ],
        Resource  = [
          "${aws_s3_bucket.super_vulnerable.arn}/*",
          "${aws_s3_bucket.super_vulnerable.arn}"
        ]
      }
    ]
  })
}