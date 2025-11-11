Get email notifications whenever GitHub **creates**, **updates** or **resolves** an incident.

Get text message notifications whenever GitHub **creates** or **resolves** an incident.

Get incident updates and maintenance status messages in Slack.

[Subscribe via Slack](https://subscriptions.statuspage.io/slack_authentication/kickoff?page_code=kctbh9vrtdwd)

By subscribing you acknowledge our [Privacy Policy](https://help.github.com/articles/github-privacy-statement/). In addition, you agree to the Atlassian [Cloud Terms of Service](https://www.atlassian.com/legal/cloud-terms-of-service) and acknowledge Atlassian's [Privacy Policy](https://www.atlassian.com/legal/privacy-policy).

Get webhook notifications whenever GitHub **creates** an incident, **updates** an incident, **resolves** an incident or **changes** a component status.

[Follow @githubstatus](https://twitter.com/githubstatus) or  [view our profile](https://twitter.com/githubstatus).

Visit our [support site](https://github.com/support).

Get the [Atom Feed](https://www.githubstatus.com/history.atom) or [RSS Feed](https://www.githubstatus.com/history.rss).

[Larger hosted runners experiencing delays](/incidents/htcm010tcwjq) [Subscribe](#subscribe-modal-htcm010tcwjq)

**Update** - The team is continuing to apply the mitigation for Large Hosted Runners. We will provide updates as we progress.   
 Nov 11, 2025 - 19:40 UTC

**Update** - The team continues to investigate delays with Large Hosted Runners. We will continue providing updates on the progress towards mitigation.   
 Nov 11, 2025 - 18:37 UTC

**Investigating** - We are currently investigating this issue.   
 Nov 11, 2025 - 18:02 UTC

## [About This Site](#about-this-site)

For the status of GitHub Enterprise Cloud - EU, please visit: [eu.githubstatus.com](https://eu.githubstatus.com)   
For the status of GitHub Enterprise Cloud - Australia, please visit: [au.githubstatus.com](https://au.githubstatus.com)   
For the status of GitHub Enterprise Cloud - US, please visit: [us.githubstatus.com](https://us.githubstatus.com/)

Git Operations  ?  Operational

Webhooks  ?  Operational

Visit www.githubstatus.com for more information   Operational

API Requests  ?  Operational

Issues  ?  Operational

Pull Requests  ?  Operational

Actions  ?  Operational

Packages  ?  Operational

Pages  ?  Operational

Codespaces  ?  Operational

Copilot   Operational

Operational

Degraded Performance

Partial Outage

Major Outage

Maintenance

## Past Incidents

Nov 11, 2025

Unresolved incident: Larger hosted runners experiencing delays.

Nov 10, 2025

No incidents reported.

Nov  9, 2025

No incidents reported.

Nov  8, 2025

No incidents reported.

Nov  7, 2025

No incidents reported.

Nov  6, 2025

[Incident with Copilot](/incidents/gnzclztblsh3)

**Resolved** - This incident has been resolved. Thank you for your patience and understanding as we addressed this issue. A detailed root cause analysis will be shared as soon as it is available.   
 Nov  6, 00:06 UTC

**Update** - We have recovered from our earlier performance issues. Copilot code completions should be functioning normally at this time.   
 Nov  6, 00:06 UTC

**Update** - Copilot Code Completions are partially unavailable. Our engineering team is engaged and investigating.   
 Nov  5, 23:41 UTC

**Investigating** - We are investigating reports of degraded performance for Copilot   
 Nov  5, 23:41 UTC

Nov  5, 2025

[Copilot Code Completions partially unavailable](/incidents/d5c8rxcwt7xw)

**Resolved** - This incident has been resolved. Thank you for your patience and understanding as we addressed this issue. A detailed root cause analysis will be shared as soon as it is available.   
 Nov  5, 23:26 UTC

**Update** - We have identified and resolved the underlying issues with Code Completions. Customers should see full recovery.   
 Nov  5, 23:26 UTC

**Update** - We are investigating increased error rates affecting Copilot Code Completions. Some users may experience delays or partial unavailability. Our engineering team is monitoring the situation and working to identify the cause.   
 Nov  5, 22:57 UTC

**Investigating** - We are investigating reports of degraded performance for Copilot   
 Nov  5, 22:56 UTC

Nov  4, 2025

No incidents reported.

Nov  3, 2025

[Incident with Packages](/incidents/y8hlsmxtgf0w)

**Resolved** - On November 3, 2025, between 14:10 UTC and 19:20 UTC, GitHub Packages experienced degraded performance, resulting in failures for 0.5% of Nuget package download requests. The incident resulted from an unexpected change in usage patterns affecting rate limiting infrastructure in the Packages service.  
  
We mitigated the issue by scaling up services and refining our rate limiting implementation to ensure more consistent and reliable service for all users. To prevent similar problems, we are enhancing our resilience to shifts in usage patterns, improving capacity planning, and implementing better monitoring to accelerate detection and mitigation in the future.   
 Nov  3, 19:20 UTC

**Update** - We have applied the mitigation and are starting to see signs of recovery. We will continue to monitor the health of the system.   
 Nov  3, 17:27 UTC

**Update** - We are continuing to work on mitigation.   
 Nov  3, 17:10 UTC

**Update** - Progress on mitigation continues but no recovery seen yet to error rates. We will continue to provide updates as we have them.   
 Nov  3, 15:58 UTC

**Update** - We are continuing to see high error rates for package downloads. Our team is working on ways to mitigate this urgently  
  
Next update in 20 minutes   
 Nov  3, 15:33 UTC

**Update** - Our investigations are continuing and we are working to mitigate impact. Thank you for your patience as we work on this.   
 Nov  3, 15:18 UTC

**Update** - We are seeing increased failure rates of up to 15% for GitHub Packages downloads with users experiencing 5xx errors.  
  
We are investigating and working towards mitigation. We will continue to provide updates as they are available.   
 Nov  3, 14:35 UTC

**Investigating** - We are investigating reports of degraded performance for Packages   
 Nov  3, 14:33 UTC

Nov  2, 2025

No incidents reported.

Nov  1, 2025

[Incident with using workflow\_dispatch for Actions](/incidents/xkvk1yhmqfdl)

**Resolved** - On November 1, 2025, between 2:30 UTC and 6:14 UTC, Actions workflows could not be triggered manually from the UI. This impacted all customers queueing workflows from the UI for most of the impact window. The issue was caused by a faulty code change in the UI, which was promptly reverted once the impact was identified. Detection was delayed due to an alerting gap for UI breaks in this area when all underlying APIs are still healthy. We are implementing enhanced alerting and additional automated tests to prevent similar regressions and reduce detection time in the future.   
 Nov  1, 06:14 UTC

**Update** - Actions is operating normally.   
 Nov  1, 06:14 UTC

**Update** - We have mitigated the issue for manually dispatching workflows via the UI   
 Nov  1, 06:14 UTC

**Update** - We have identified the cause of the issue and are working towards a mitigation   
 Nov  1, 05:35 UTC

**Update** - We are investigating issues manually dispatching workflows via the GitHub UI for Actions. The Workflow Dispatch API is unaffected.   
 Nov  1, 05:05 UTC

**Investigating** - We are investigating reports of degraded performance for Actions   
 Nov  1, 04:43 UTC

Oct 31, 2025

No incidents reported.

Oct 30, 2025

[Disruption with some GitHub services](/incidents/6hygvwpw2vr3)

**Resolved** - On October 30th we shipped a change that broke 3 links in the "Solutions" dropdown of the marketing navigation seen on <https://github.com/home>. We noticed internally the broken links and declared an incident so our users would know no other functionality was impacted. We were able to revert a change and are evaluating our testing and rollout processes to prevent future incidents like these.   
 Oct 30, 23:00 UTC

**Update** - Links on GitHub's landing <https://github.com/home> are not working. Primary user workflows (PRs, Issues, Repos) are not impacted.   
 Oct 30, 22:54 UTC

**Update** - Dotcom main navigation broken links.   
 Oct 30, 22:47 UTC

**Investigating** - We are currently investigating this issue.   
 Oct 30, 22:47 UTC

Oct 29, 2025

[Experiencing connection issues across Actions, Codespaces, and possibly other services](/incidents/4jxdz4m769gy)

**Resolved** - On October 29th, 2025 between 14:07 UTC and 23:15 UTC, multiple GitHub services were degraded due to a broad outage in one of our service providers:  
  
- Users of Codespaces experienced failures connecting to new and existing Codespaces through VSCode Desktop or Web. On average the Codespace connection error rate was 90% and peaked at 100% across all regions throughout the incident period.  
- GitHub Actions larger hosted runners experienced degraded performance, with 0.5% of overall workflow runs and 9.8% of larger hosted runner jobs failing or not starting within 5 minutes. These recovered by 20:40 UTC.  
- The GitHub Enterprise Importer service was degraded, with some users experiencing migration failures during git push operations and most users experiencing delayed migration processing.  
- Initiation of new trials for GitHub Enterprise Cloud with Data Residency were also delayed during this time.  
- Copilot Metrics via the API could not access the downloadable link during this time. There were approximately 100 requests during the incident that would have failed the download. Recovery began around 20:25 UTC.  
  
We were able to apply a number of mitigations to reduce impact over the course of the incident, but we did not achieve 100% recovery until our service provider’s incident was resolved.  
  
We are working to reduce critical path dependencies on the service provider and gracefully degrade experiences where possible so that we are more resilient to future dependency outages.   
 Oct 29, 23:15 UTC

**Update** - Codespaces is operating normally.   
 Oct 29, 23:15 UTC

**Update** - Codespaces continues to recover   
 Oct 29, 22:06 UTC

**Update** - Actions is operating normally.   
 Oct 29, 21:02 UTC

**Update** - Actions has fully recovered.  
  
Codespaces continues to recover. Regions across Europe and Asia are healthy, so US users may want to choose one of those regions following these instructions: <https://docs.github.com/en/codespaces/setting-your-user-preferences/setting-your-default-region-for-github-codespaces>.  
  
We expect full recovery across the board before long.   
 Oct 29, 21:01 UTC

**Update** - Codespaces is experiencing degraded performance. We are continuing to investigate.   
 Oct 29, 20:56 UTC

**Update** - We are beginning to see small signs of recovery, but connections are still inconsistent across services and regions. We expect to see gradual recovery from here.   
 Oct 29, 20:34 UTC

**Update** - We continue to see improvement in Actions larger runners jobs. Larger runners customers may still experience longer than normal queue times, but we expect this to rapidly improve across most runners.   
  
ARM64 runners, GPU runners, and some runners with private networking may still be impacted.  
  
Usage of Codespaces via VS Code (but not via SSH) is still degraded.  
  
GitHub and Azure teams continue to collaborate towards full resolution.   
 Oct 29, 19:21 UTC

**Update** - Codespaces is experiencing degraded availability. We are continuing to investigate.   
 Oct 29, 19:05 UTC

**Update** - Codespaces is experiencing degraded performance. We are continuing to investigate.   
 Oct 29, 18:58 UTC

**Update** - Impact to most larger runner jobs should now be mitigated. ARM64 runners are still impacted. GitHub and Azure teams continue to collaborate towards full resolution.   
 Oct 29, 18:12 UTC

**Update** - Codespaces is experiencing degraded availability. We are continuing to investigate.   
 Oct 29, 17:40 UTC

**Update** - Additional impact from this incident:  
  
We’re currently investigating an issue causing the Copilot Metrics API report URLs to fail for 28-day and 1-day enterprise and user reports. We are collaborating with Azure teams to restore access as soon as possible.   
 Oct 29, 17:26 UTC

**Update** - We are seeing ongoing connection failures across Codespaces and Actions, including Enterprise Migrations.   
  
Linux ARM64 standard hosted runners are failing to start, but Ubuntu latest and Windows latest are not affected at this time.   
  
SSH connections to Codespaces may be successful, but connections via VS Code are consistently failing.   
  
GitHub and Azure teams are coordinating to mitigate impact and resolve the root issues.   
 Oct 29, 17:11 UTC

**Update** - Actions impact is primarily limited to larger runner jobs at this time. This also impacts enterprise migrations.   
 Oct 29, 16:31 UTC

**Update** - Codespaces is experiencing degraded performance. We are continuing to investigate.   
 Oct 29, 16:19 UTC

**Investigating** - We are investigating reports of degraded performance for Actions   
 Oct 29, 16:17 UTC

[Disruption with Copilot Bing search tool](/incidents/pch0flk719dj)

**Resolved** - A cloud resource used by the Copilot bing-search tool was deleted as part of a resource cleanup operation. Once this was discovered, the resource was recreated. Going forward, more effective monitoring will be put in place to catch this issue earlier.   
 Oct 29, 21:49 UTC

**Investigating** - We are currently investigating this issue.   
 Oct 29, 21:34 UTC

Oct 28, 2025

[Inconsistent results when using the Haiku 4.5 model](/incidents/jlhnszknd9pj)

**Resolved** - From October 28th at 16:03 UTC until 17:11 UTC, the Copilot service experienced degradation due to an infrastructure issue which impacted the Claude Haiku 4.5 model, leading to a spike in errors affecting 1% of users. No other models were impacted. The incident was caused due to an outage with an upstream provider. We are working to improve redundancy during future occurrences.   
 Oct 28, 17:11 UTC

**Update** - The issues with our upstream model provider have been resolved, and Claude Haiku 4.5 is once again available in Copilot Chat and across IDE integrations.  
  
We will continue monitoring to ensure stability, but mitigation is complete.   
 Oct 28, 17:11 UTC

**Update** - Usage of the Haiku 4.5 model with Copilot experiences is currently degraded. We are investigating and working to remediate. Other models should be unaffected.   
 Oct 28, 16:42 UTC

**Investigating** - We are currently investigating this issue.   
 Oct 28, 16:39 UTC

[← Incident History](/history) [Powered by Atlassian Statuspage](https://www.atlassian.com/software/statuspage?utm_campaign=www.githubstatus.com&utm_content=SP-notifications&utm_medium=powered-by&utm_source=inapp)

### Subscribe to our developer newsletter

Get tips, technical guides, and best practices. Twice a month. Right in your inbox.

[Subscribe](https://resources.github.com/newsletter/)

 