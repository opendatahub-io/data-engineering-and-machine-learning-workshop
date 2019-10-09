# Setup your cluster for this workshop

To prepare your cluster for the workshop from the infrastructure (mainly S3 Object Storage deployment) and attendees (generation of use accounts and namespaces) perspective you will need to run Ansible playbooks from a project called [**AgnosticD**](https://github.com/redhat-cop/agnosticd).

Make sure you have `git`, `ansible`, `oc` and Python `openshift` packages installed, otherwise following commands might fail.

First you will need to clone the repository and enter the directory with Ansible playbooks.
```
git clone https://github.com/redhat-cop/agnosticd
cd agnosticd/ansible
```

Next you will need couple environment variables set for the following commands to work.
```
OCP_ADMIN_USERNAME=opentlc-mgr
START_NUM_FOR_USER=1
NUM_OF_USERS=5
```

The following command deploys the infrastructure part of the workshop

```
ansible-playbook --connection local -i localhost, \
configs/ocp-workloads/ocp-workload.yml \
-e 'ocp_username='${OCP_ADMIN_USERNAME} \
-e 'ocp_workload=ocp4-workload-rhte-analytics_data_ocp_infra' \
-e 'silent=False' \
-e 'ACTION=create'
```

Once Rook Ceph is deployed and Object Storage is created (i.e. the above command successfully finishes) you need to extract an IP address and port of the S3 endpoint. The following command takes care of it and sets the needed environment variables as well.

```
eval $(oc get service -n rook-ceph rook-ceph-rgw-my-store -o jsonpath='{"ROOK_CEPH_RGW_SERVICE_IP="}{.spec.clusterIP}{"\n"}{"ROOK_CEPH_RGW_PORT="}{.spec.ports[0].port}{"\n"}')
```

The last command before you can start the workshop is to create users, user namespaces and deploy the Open Data Hub operator for each user.

```
ansible-playbook --connection local -i localhost, \
configs/ocp-workloads/ocp-workload.yml \
-e 'ocp_username='${OCP_ADMIN_USERNAME} \
-e 'ocp_workload=ocp4-workload-rhte-analytics_data_ocp_workshop' \
-e 'silent=False' \
-e 'ACTION=create' \
-e 'rgw_service_ip='${ROOK_CEPH_RGW_SERVICE_IP} \
-e 'rgw_service_port='${ROOK_CEPH_RGW_PORT} \
-e 'num_users='${NUM_OF_USERS} \
-e 'user_count_start='${START_NUM_FOR_USER} \
-e 'deploy_odh_cr=false'
```

This procedure assumes your cluster has a number of users precreated. The usernames should be in a form `userN` where `N` is a number starting with `${START_NUM_FOR_USER}` and ending with `${START_NUM_FOR_USER}+${NUM_OF_USERS}`.

The attendees should login to cluster and follow information in the file [./doc/for-attendees.md](/doc/for-attendees.md).