<# Đếm độc lập với Python và đối chiếu bảng ví dụ trong báo cáo. Chỉ đọc nguồn, in JSON. #>
param(
    [string]$SourcePath = (Join-Path $PSScriptRoot '../data/preclass/chat.csv'),
    [string]$ReportPath = (Join-Path $PSScriptRoot '../evidence/data-mining.md')
)
$ErrorActionPreference = 'Stop'
$culture = [Globalization.CultureInfo]::InvariantCulture
$rows = @(Import-Csv -LiteralPath $SourcePath -Encoding utf8)
$questions = @($rows | Where-Object { $_.kind -eq 'question' -and $_.agent_id -eq 'teaching_assistant' })
if ($questions.Count -eq 0) { throw 'Không có câu hỏi thoả bộ lọc.' }
$records = @($questions | ForEach-Object {
    [pscustomobject]@{
        Id = $_.id
        Learner = $_.hv
        Channel = $_.channel
        Video = $_.transcript
        Asked = [DateTimeOffset]::Parse($_.asked_at, $culture)
        Latency = ([DateTimeOffset]::Parse($_.created_at, $culture) - [DateTimeOffset]::Parse($_.asked_at, $culture)).TotalSeconds
        QuestionLength = [int]$_.do_dai_cau_hoi
        AnswerLength = [int]$_.do_dai_tra_loi
    }
})
$byId = @{}
foreach ($record in $records) {
    if ($byId.ContainsKey($record.Id)) { throw 'ID câu hỏi bị trùng.' }
    $byId[$record.Id] = $record
}
$followups = [Collections.Generic.List[object]]::new()
$previousById = @{}
$groups = $records | Where-Object { $_.Channel -eq 'video_question' -and $_.Video } | Group-Object Learner,Video
foreach ($group in $groups) {
    $ordered = @($group.Group | Sort-Object Asked)
    for ($index = 1; $index -lt $ordered.Count; $index++) {
        $gap = ($ordered[$index].Asked - $ordered[$index - 1].Asked).TotalSeconds
        if ($gap -le 120) {
            $followups.Add($ordered[$index])
            $previousById[$ordered[$index].Id] = $ordered[$index - 1]
        }
    }
}
$channelCounts = [ordered]@{}
foreach ($group in ($records | Group-Object Channel | Sort-Object Name)) { $channelCounts[$group.Name] = $group.Count }
$exampleCount = 0
$pairCount = 0
foreach ($line in (Get-Content -LiteralPath $ReportPath -Encoding utf8)) {
    if ($line -match '^\| (C\d+) \| (\d+) \| (\d+) \| (\d+) \| ([\d,]+) \|$') {
        $code = $Matches[1]
        $record = $byId[$code]
        $expectedPosition = [int]$Matches[2]
        $expectedQuestionLength = [int]$Matches[3]
        $expectedAnswerLength = [int]$Matches[4]
        $expectedLatency = [double]::Parse($Matches[5].Replace(',', '.'), $culture)
        $position = [array]::IndexOf([string[]]$rows.id, $code) + 1
        if ($null -eq $record -or $position -ne $expectedPosition -or
            $record.QuestionLength -ne $expectedQuestionLength -or $record.AnswerLength -ne $expectedAnswerLength -or
            [math]::Abs($record.Latency - $expectedLatency) -gt 0.0000001) {
            throw "Ví dụ không khớp nguồn: $code"
        }
        $exampleCount++
    }
    elseif ($line -match '^\| (C\d+) \| (C\d+) \| ([\d,]+) \| Có \|$') {
        $previousId = $Matches[1]
        $currentId = $Matches[2]
        $expectedGap = [double]::Parse($Matches[3].Replace(',', '.'), $culture)
        $previous = $byId[$previousId]
        $current = $byId[$currentId]
        if ($null -eq $previous -or $null -eq $current -or $previousById[$currentId].Id -ne $previousId -or
            $previous.Learner -ne $current.Learner -or $previous.Video -ne $current.Video -or
            [math]::Abs(($current.Asked - $previous.Asked).TotalSeconds - $expectedGap) -gt 0.0000001) {
            throw "Cặp hỏi tiếp không khớp nguồn: $previousId -> $currentId"
        }
        $pairCount++
    }
}
if ($exampleCount -lt 5 -or $pairCount -lt 5) { throw 'Báo cáo phải có ít nhất 5 ví dụ dòng và 5 cặp để kiểm.' }
$videoRecords = @($records | Where-Object Channel -EQ 'video_question')
[ordered]@{
    source_sha256 = (Get-FileHash -LiteralPath $SourcePath -Algorithm SHA256).Hash.ToLowerInvariant()
    total_rows = $rows.Count
    questions = $records.Count
    learners = @($records.Learner | Sort-Object -Unique).Count
    channels = $channelCounts
    short_questions = @($records | Where-Object QuestionLength -LE 10).Count
    fast_responses = @($records | Where-Object { $_.Latency -ge 0 -and $_.Latency -lt 0.5 }).Count
    followups = $followups.Count
    followup_learners = @($followups.Learner | Sort-Object -Unique).Count
    video_questions = $videoRecords.Count
    verified_report_examples = $exampleCount
    verified_report_pairs = $pairCount
} | ConvertTo-Json -Depth 4
