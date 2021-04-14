# Deployment Instructions

This workshop  is deployed using the OpenDatahub Operator found [here](https://gitlab.com/opendatahub/opendatahub-operator).

## Instructions to deploy

1. Follow the instructions for installation as found at opendatahub.io [quick-installation](http://opendatahub.io/docs/getting-started/quick-installation.html).
1. Use the provided [KfDef](templates/data-engineering-workshop.kfdef.yaml) to deploy ODH components used in this workshop
1. To Deploy Ceph Object Storage, follow the instructions under `Administration -> Advanced Installation` in [Object Storage](http://opendatahub.io/docs/administration/advanced-installation/object-storage.html)
