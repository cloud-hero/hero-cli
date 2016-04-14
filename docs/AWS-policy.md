


```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "ec2:DescribeInstances",
                "ec2:DescribeAvailabilityZones",
                "ec2:DescribeSubnets",
                "ec2:DescribeImages",
                "ec2:DescribeTags",
                "ec2:DescribeRegions",
                "ec2:CreateTags",
                "ec2:CreateNetworkInterface",
                "ec2:CreateKeyPair",
                "ec2:CreateSecurityGroup",
                "ec2:DescribeKeyPairs",
                "ec2:DescribeSecurityGroups",
                "ec2:AuthorizeSecurityGroupEgress",
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:ImportKeyPair",
                "ec2:DeleteTags",
                "ec2:StartInstances",
                "ec2:RunInstances",
                "ec2:ModifyInstanceAttribute",
                "ec2:ModifyNetworkInterfaceAttribute",
                "ec2:StopInstances",
                "ec2:TerminateInstances"
            ],
            "Resource": "*",
            "Effect": "Allow",
            "Condition": {
                "StringEquals": {
                    "ec2:Region": "eu-west-1"
                }
            }
        }
    ]
}
```
