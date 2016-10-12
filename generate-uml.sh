(
  . env.sh ;
  . $HOME/envs/oxidentity/bin/activate ;

  python manage.py graph_models oxidentity nationality attestation name gender org_relationship > models.dot ;
  dot -Tpng models.dot > models.png ;
)
