#!/usr/bin/env python3
"""Regression checks for this repository, not a Shadowrocket runtime emulator.

Remote rule sets, other phone modules, DNS reachability and actual playback are
outside this check. Known compound ad rules are allowlisted for manual review.
"""
from pathlib import Path
import fnmatch
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PROFILE = 'profiles/Smart-Hybrid-AI-Remote-DNS-Test-Fixed.conf'
TV = (
    'tv.apple.com', 'vod-ap-aoc.tv.apple.com', 'amp-api.videos.apple.com',
    'videos.apple.com', 'itunes.apple.com', 'hls-amt.itunes.apple.com',
    'hls.itunes.apple.com', 'np-edge.itunes.apple.com', 'play-edge.itunes.apple.com',
    'uts-api.itunes.apple.com', 'tv.applemusic.com', 'appletv.com', 'www.appletv.com',
    'is1-ssl.mzstatic.com', 'apps.mzstatic.com', 's.mzstatic.com',
)
PAY = (
    'apple-pay-gateway.apple.com', 'cn-apple-pay-gateway.apple.com',
    'apple-pay-gateway-nc-pod4.apple.com', 'apple-pay-gateway-pr-pod3.apple.com',
    'smp-device.apple.com', 'sh-pod1-smp-device.apple.com', 'pr-pod2-smp-device.apple.com',
)
YOUTUBE = ('youtube.com', 'www.youtube.com', 'ad.youtube.com', 'ads.youtube.com',
           'youtube.googleapis.com', 'i.ytimg.com', 'www.youtube-nocookie.com',
           'r1---sn-test.googlevideo.com', 'youtu.be')
COMPOUND = {
    'AND,((DOMAIN,acs.m.goofish.com),(PROTOCOL,UDP)),REJECT',
    'AND,((DOMAIN,g-acs.m.goofish.com),(PROTOCOL,UDP)),REJECT',
    'AND,((URL-REGEX,"^http:\\/\\/.+\\/amdc\\/mobileDispatch"),(USER-AGENT,"%E9%97%B2%E9%B1%BC*")),REJECT',
}


def sections(text):
    result, name = {}, ''
    for line in text.splitlines():
        line = line.strip()
        if line.startswith('[') and line.endswith(']'):
            name = line[1:-1]
            result.setdefault(name, [])
        elif line and not line.startswith('#'):
            result.setdefault(name, []).append(line)
    return result


def matches(rule, host):
    kind, value, *_ = [x.strip() for x in rule.split(',')]
    if kind == 'DOMAIN':
        return host == value
    if kind == 'DOMAIN-SUFFIX':
        return host == value or host.endswith('.' + value)
    if kind == 'DOMAIN-KEYWORD':
        return value in host
    if kind == 'DOMAIN-WILDCARD':
        return fnmatch.fnmatchcase(host, value)
    return False


def validate(profile, module):
    errors = []
    def require(ok, message):
        if not ok:
            errors.append(message)
    p, m = sections(profile), sections(module)
    for name, text in [('profile', profile), ('module', module)]:
        require(not re.search(r'^\s*ca-(?:p12|passphrase)\s*=\s*\S', text, re.M),
                f'{name}: private certificate material must not be public')
        require('油管视频' not in text, f'{name}: obsolete YouTube policy')
        groups = sections(text).get('Proxy Group', [])
        require(not any(re.search(r'=\s*(url-test|fallback|load-balance)\b', x) for x in groups),
                f'{name}: automatic node group contradicts manual selection')
    rules = p.get('Rule', [])
    boundary = next((i for i, x in enumerate(rules) if x.startswith('RULE-SET,')), len(rules))
    for host in TV + PAY:
        local = next((r for r in rules[:boundary] if matches(r, host)), '')
        require(bool(local) and local.split(',')[2] == 'DIRECT', f'{host}: explicit DIRECT missing/overridden')
        for name, config in [('profile', p), ('module', m)]:
            hostname = next((x.split('=', 1)[1] for x in config.get('MITM', []) if x.startswith('hostname')), '')
            exclusions = [h.strip().removeprefix('%APPEND%').strip()[1:] for h in hostname.split(',')
                          if h.strip().removeprefix('%APPEND%').strip().startswith('-')]
            require(any(fnmatch.fnmatchcase(host, h) for h in exclusions), f'{name}: MITM exclusion missing for {host}')
    module_rules = m.get('Rule', [])
    require(len(module_rules) == len(set(module_rules)), 'module: duplicate rule')
    for rule in module_rules:
        if rule in COMPOUND:
            continue
        parts = rule.split(',')
        require(parts[0] in {'DOMAIN', 'DOMAIN-SUFFIX', 'DOMAIN-KEYWORD', 'DOMAIN-WILDCARD'},
                'module: new rule type/compound rule needs manual review')
        require(len(parts) >= 3 and parts[2] in {'DIRECT', 'PROXY', 'REJECT', 'REJECT-DROP', 'REJECT-200'},
                'module: undefined or unreviewed policy')
        for host in TV + PAY:
            require(not matches(rule, host) or parts[2] == 'DIRECT', f'module conflicts with {host}')
        for host in YOUTUBE:
            require(not matches(rule, host), f'module: unexpected YouTube routing/blocking for {host}')
    names = [x.split('=', 1)[0].strip() for x in m.get('Script', [])]
    require(len(names) == len(set(names)), 'module: duplicate script name')
    for section in ['Script', 'URL Rewrite', 'Body Rewrite', 'Map Local']:
        require(not any('youtube' in x.lower() or 'googlevideo' in x.lower() for x in m.get(section, [])),
                f'{section}: YouTube modification reintroduced')
    for rule in m.get('Map Local', []):
        for host in ('i0.hdslb.com', 'i1.hdslb.com'):
            require(not re.search(rule.split()[0], f'https://{host}/bfs/archive/ordinary-cover.jpg'),
                    'Map Local: general Bilibili cover path intercepted')
    return errors


if __name__ == '__main__':
    errors = validate((ROOT / PROFILE).read_text(), (ROOT / 'Module.sgmodule').read_text())
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        sys.exit(1)
    print(f'Personal routing checks passed: {len(TV)} TV/resource and {len(PAY)} Pay host samples; module policies, MITM exclusions and YouTube checked.')
