#!/bin/sh

# Set default values
repetitions=1
project_path="./test_modules/typesystem"
module_name="typesystem.formats"
output_path="./test_outputs/typesystem/formats/MOSA"
report_dir="./test_outputs/typesystem/formats/MOSA"
max_time="600"

# Help
help_info()
{
  echo "-r <repeitions number> or --repetitions <repeitions number> are used to define the number of repetitions to run each task"
  exit
}

# Log with a timestamp
log()
{
  # Output is redirected to the log file if needed at the script's lop level
  date +'%F %T ' | tr -d \\n 1>&2
  echo "$@" 1>&2
}

# Function that executes
collect_energy_measurements()
{
  log "Obtaining energy and run-time performance measurements"

  for i in $(seq 1 $2); do
    # Collect the energy consumption of the GPU
    nvidia-smi --loop-ms=1000 --format=csv,noheader --query-gpu=power.draw,temperature.gpu,temperature.memory,utilization.gpu,utilization.memory >> nvidia_smi"$i".log &

    # Get nvidia-smi's PID
    nvidia_smi_PID=$!

    # Run model
    perf stat -e power/energy-pkg/,power/energy-ram/ $1>out.log 2>> ./cpu.log
    # $1>out.log

    # When the experiment is elapsed, terminate the nvidia-smi process
    kill -9 "$nvidia_smi_PID"

    log "Small sleep time to reduce power tail effecs"
    sleep 60

  done
}

# Get command-line arguments
OPTIONS=$(getopt -o p:m:o:r:t: --long repetitions:test -n 'run_experiments' -- "$@")
eval set -- "$OPTIONS"
while true; do
  case "$1" in
    -p|--project_path) project_path="$2"; shift 2;;
    -m|--module_name) module_name="$2"; shift 2;;
    -o|--output_path) output_path="$2"; shift 2;;
    -r|--report_dir) report_dir="$2"; shift 2;;
    -t|--max_time) max_time="$2"; shift 2;;
    --) shift; break;;
    *) >&2 log "${redlabel}[ERROR]${default} Wrong command line argument, please try again."; exit 1;;
  esac
done

# Switching to perfomrance mode
log "Switching to performance mode"
sudo ./governor.sh pe
export PYNGUIN_DANGER_AWARE=0

# Settings
py_cmd="python ./pynguin/__main__.py"
p_path=" --project_path ${project_path}"
m_name=" --module_name ${module_name}"
o_path=" --output_path ${output_path}"
r_path=" --report_dir ${report_dir}"
max_t=" --maximum_search_time ${max_time}"
alg=" --algorithm MOSA -v"

# Running codamosa
cmd="${py_cmd}${p_path}${m_name}${o_path}${r_path}${max_t}${alg}"
log "${cmd}"
collect_energy_measurements "${cmd}" "${repetitions}"

log "Done with all tests"

