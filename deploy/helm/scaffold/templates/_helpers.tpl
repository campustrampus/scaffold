{{/*
Expand the name of the chart.
*/}}
{{- define "scaffold.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "scaffold.fullname" -}}
{{- printf "%s" .Release.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "scaffold.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "scaffold.labels" -}}
helm.sh/chart: {{ include "scaffold.chart" . }}
app.kubernetes.io/name: {{ include "scaffold.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
team: makesTheDream
{{- end }}

{{/*
Celery backend url
*/}}
{{- define "scaffold.celery.backendURL" -}}
  {{- printf "db+%s" .Values.backend.db.uri }}
{{- end }}

