provider "aws" {
  region = "eu-west-1"
  profile = "default"
}

resource "aws_s3_bucket" "rekognize-bucket" {
  bucket = "${lower(var.app)}-rekognize"
  acl = "public-read"

  tags {
        Environment = "${var.env}"
        Application = "${var.app}"
  }
}

resource "aws_dynamodb_table" "annonce-table" {
  name = "${var.app}-annonce"
  read_capacity = 10
  write_capacity = 10
  hash_key = "annonce_id"

  attribute {
    name = "annonce_id"
    type = "S"
  }

  attribute {
    name = "agence_id"
    type = "S"
  }

  ttl {
    attribute_name = "ttl"
    enabled = true
  }

  global_secondary_index {
    name = "agences-index"
    hash_key = "agence_id"
    read_capacity = 5
    write_capacity = 5
    projection_type = "ALL"
  }

  tags {
        Environment = "${var.env}"
        Application = "${var.app}"
  }
}

resource "aws_dynamodb_table" "photo-table" {
  name = "${var.app}-photo"
  read_capacity = 10
  write_capacity = 10
  hash_key = "photo_id"
  stream_enabled = "true"
  stream_view_type = "NEW_IMAGE"

  attribute {
    name = "photo_id"
    type = "S"
  }

  attribute {
    name = "annonce_id"
    type = "S"
  }

  ttl {
    attribute_name = "ttl"
    enabled = true
  }

  global_secondary_index {
    name = "annonces_index"
    hash_key = "annonce_id"
    read_capacity = 5
    write_capacity = 5
    projection_type = "ALL"
  }



  tags {
        Environment = "${var.env}"
        Application = "${var.app}"
  }
}

resource "aws_dynamodb_table" "tag-table" {
  name = "${var.app}-tag"
  read_capacity = 10
  write_capacity = 10
  hash_key = "tag_id"

  attribute {
    name = "tag_id"
    type = "S"
  }

  ttl {
    attribute_name = "ttl"
    enabled = true
  }

  tags {
        Environment = "${var.env}"
        Application = "${var.app}"
  }
}

output "photo_stream_arn" {
     value = "${aws_dynamodb_table.photo-table.stream_arn}"
}

output "annonce_table" {
     value = "${aws_dynamodb_table.annonce-table.name}"
}

output "photo_table" {
     value = "${aws_dynamodb_table.photo-table.name}"
}

output "tag_table" {
     value = "${aws_dynamodb_table.tag-table.name}"
}

output "rekognition_bucket" {
     value = "${aws_s3_bucket.rekognize-bucket.bucket}"
}