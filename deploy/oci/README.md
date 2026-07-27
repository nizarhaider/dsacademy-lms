# Oracle Cloud Always Free deployment

The production target is one Ubuntu 24.04 Ampere A1 VM using only resources
labelled **Always Free-eligible** in the OCI console.

Recommended VM allocation:

- Shape: `VM.Standard.A1.Flex`
- Compute: 2 OCPUs and 12 GB memory
- Boot volume: 100 GB, Always Free-eligible
- Ingress: TCP 22, 80, and 443
- DNS: `learn.dsacademy.lk` A record pointing to the VM public IPv4 address

Do not provision trial-only load balancers, databases, or paid block volumes.
Frappe's production installer runs MariaDB, Redis, workers, websocket, scheduler,
reverse proxy, and TLS on the VM.

Always Free capacity can be unavailable in a region, carries no production SLA,
and idle compute may be reclaimed under Oracle's current policy. Keep verified
off-VM backups even though the application stack itself has no recurring
hosting charge.

The `dsacademy.lk` nameservers are currently managed by Netlify DNS. In
Netlify's DNS panel for `dsacademy.lk`, add an `A` record named `learn` with the
VM's assigned public IPv4 address. Wait until
`dig +short learn.dsacademy.lk A` returns that address before running the
bootstrap, because the installer requests the TLS certificate during deployment.

## Deploy

After the DNS record resolves and GitHub Container Registry has published the
`stable` image, confirm that the `dsacademy-lms` package is public in GitHub
Packages so the VM can pull it without storing a registry token:

```bash
sudo apt-get update
sudo apt-get install --yes curl git python3
git clone https://github.com/nizarhaider/dsacademy-lms.git
cd dsacademy-lms
export SITE_NAME=learn.dsacademy.lk
export LETSENCRYPT_EMAIL=nizarhaider@gmail.com
bash deploy/oci/bootstrap.sh
```

The bootstrap is rerunnable. Database and site volumes remain attached to the
Docker Compose project. On Ampere ARM hosts it also removes Frappe Docker's
current `linux/amd64` service overrides so the multi-architecture DS Academy
image runs natively.

References:

- [Frappe Learning production installation](https://docs.frappe.io/learning/get-started/installation)
- [Oracle Always Free resources](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm)

## Launch checklist

1. Sign in as Administrator and replace the generated administrator password.
2. Set a strong password for `instructor@dsacademy.lk`; the domain currently
   has no MX record, so do not depend on email delivery to that address.
3. Configure an outgoing Email Account so signup, invitations, and password
   recovery work. A Gmail account with an app password is a no-cost option;
   never store the app password in this repository.
4. Create a learner account, enroll, complete one quiz, and submit one
   assignment.
5. Run a backup and copy it to encrypted storage outside the VM.
6. Run `bash deploy/oci/verify.sh` from the repository and confirm every
   production route and representative media asset passes.

## Operations

Create a database backup:

```bash
docker compose --project-name dsacademy_lms \
  --file ~/dsacademy_lms-compose.yml exec backend \
  bench --site learn.dsacademy.lk backup --with-files
```

Apply a newly published image:

```bash
docker compose --project-name dsacademy_lms \
  --file ~/dsacademy_lms-compose.yml pull
docker compose --project-name dsacademy_lms \
  --file ~/dsacademy_lms-compose.yml up --detach
docker compose --project-name dsacademy_lms \
  --file ~/dsacademy_lms-compose.yml exec backend \
  bench --site learn.dsacademy.lk migrate
docker compose --project-name dsacademy_lms \
  --file ~/dsacademy_lms-compose.yml exec backend \
  bench --site learn.dsacademy.lk execute lms.dsacademy.seed.seed_all
```
