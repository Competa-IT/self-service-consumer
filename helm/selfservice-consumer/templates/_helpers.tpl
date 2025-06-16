{{- /*
SPDX-FileCopyrightText: 2024 Univention GmbH
SPDX-License-Identifier: AGPL-3.0-only
*/}}
{{- /*
These template definitions relate to the use of this Helm chart as a sub-chart of the Nubus Umbrella Chart.
Templates defined in other Helm sub-charts are imported to be used to configure this chart.
If the value .Values.global.nubusDeployment equates to true, the defined templates are imported.
*/}}

{{- /*
These template definitions are only used in this chart and do not relate to templates defined elsewhere.
*/}}
{{- define "selfservice-listener.umc.connection.baseUrl" -}}
{{- if .Values.umc.connection.baseUrl -}}
{{- tpl .Values.umc.connection.baseUrl . -}}
{{- else if .Values.global.nubusDeployment -}}
{{- $protocol := "http" -}}
{{- printf "%s://%s-umc-server" $protocol .Release.Name -}}
{{- else -}}
{{- required ".Values.umc.connection.baseUrl must be defined." .Values.umc.connection.baseUrl -}}
{{- end -}}
{{- end -}}
