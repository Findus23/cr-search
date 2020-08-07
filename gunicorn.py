# import multiprocessing

pidfile = "/srv/server/crsearch/runtime/pid"
bind = "unix:/srv/server/crsearch/runtime/socket"
proc_name = "crsearch"
worker_tmp_dir = "/dev/shm"
# workers = multiprocessing.cpu_count() * 2 + 1
