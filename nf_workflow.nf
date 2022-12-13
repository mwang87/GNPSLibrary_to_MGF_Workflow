#!/usr/bin/env nextflow
nextflow.enable.dsl=2

params.library_name = "GNPS-LIBRARY"

// Workflow Boiler Plate
params.OMETALINKING_YAML = "flow_filelinking.yaml"
params.OMETAPARAM_YAML = "job_parameters.yaml"

TOOL_FOLDER = "$baseDir/bin"

process processData {
    publishDir "./nf_output", mode: 'copy'

    conda "$TOOL_FOLDER/conda_env.yml"

    input:
    val x

    // output:
    // file 'output.tsv' into records_ch

    """
    python $TOOL_FOLDER/script.py $params.library_name output.tsv
    """
}

workflow {
  def num = Channel.of(1)
  processData(num)
}