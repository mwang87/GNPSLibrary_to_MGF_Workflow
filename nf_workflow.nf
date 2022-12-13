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

    output:
    file 'summary.tsv'
    file 'converted.mgf'

    """
    python $TOOL_FOLDER/convert.py "$params.library_name" summary.tsv converted.mgf
    """
}

workflow {
  def num = Channel.of(1)
  processData(num)
}