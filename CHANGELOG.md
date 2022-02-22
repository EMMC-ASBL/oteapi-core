# Changelog

## [Unreleased](https://github.com/EMMC-ASBL/oteapi-core/tree/HEAD)

[Full Changelog](https://github.com/EMMC-ASBL/oteapi-core/compare/v0.1.0...HEAD)

**Fixed bugs:**

- xlsx parse strategy fails parsing file on Windows [\#23](https://github.com/EMMC-ASBL/oteapi-core/issues/23)

## [v0.1.0](https://github.com/EMMC-ASBL/oteapi-core/tree/v0.1.0) (2022-02-22)

[Full Changelog](https://github.com/EMMC-ASBL/oteapi-core/compare/v0.0.6...v0.1.0)

**Implemented enhancements:**

- Clean up tests [\#75](https://github.com/EMMC-ASBL/oteapi-core/issues/75)
- Image parser: Use datacache [\#63](https://github.com/EMMC-ASBL/oteapi-core/issues/63)

**Fixed bugs:**

- Entrypoint does not seem to be updated during rebuild [\#86](https://github.com/EMMC-ASBL/oteapi-core/issues/86)
- Use proper file scheme URLs in tests [\#74](https://github.com/EMMC-ASBL/oteapi-core/issues/74)

**Closed issues:**

- Use standard library functions instead of homemade code for handling file:// URIs [\#88](https://github.com/EMMC-ASBL/oteapi-core/issues/88)
- Remove image/eps as supported image format [\#68](https://github.com/EMMC-ASBL/oteapi-core/issues/68)

**Merged pull requests:**

- EntryPoint duplicity [\#87](https://github.com/EMMC-ASBL/oteapi-core/pull/87) ([CasperWA](https://github.com/CasperWA))
- Added support for dumping numpy arrays to the datacache [\#83](https://github.com/EMMC-ASBL/oteapi-core/pull/83) ([jesper-friis](https://github.com/jesper-friis))
- \[Auto-generated\] Update dependencies [\#82](https://github.com/EMMC-ASBL/oteapi-core/pull/82) ([TEAM4-0](https://github.com/TEAM4-0))
- Pydantic dataclasses [\#81](https://github.com/EMMC-ASBL/oteapi-core/pull/81) ([CasperWA](https://github.com/CasperWA))
- Made datacache accepting AttrDict configuration [\#70](https://github.com/EMMC-ASBL/oteapi-core/pull/70) ([jesper-friis](https://github.com/jesper-friis))

## [v0.0.6](https://github.com/EMMC-ASBL/oteapi-core/tree/v0.0.6) (2022-02-14)

[Full Changelog](https://github.com/EMMC-ASBL/oteapi-core/compare/v0.0.5...v0.0.6)

**Implemented enhancements:**

- New Function strategy [\#19](https://github.com/EMMC-ASBL/oteapi-core/issues/19)

**Fixed bugs:**

- ResourceConfig.configuration should be a dict [\#65](https://github.com/EMMC-ASBL/oteapi-core/issues/65)
- Configuration bug [\#34](https://github.com/EMMC-ASBL/oteapi-core/issues/34)
- Change mediaType for json to application/json [\#24](https://github.com/EMMC-ASBL/oteapi-core/issues/24)

**Closed issues:**

- AttrDict cannot be \*\*unpacked [\#69](https://github.com/EMMC-ASBL/oteapi-core/issues/69)
- Add tests of configuration object subscripting functionality [\#61](https://github.com/EMMC-ASBL/oteapi-core/issues/61)
- Tests require installation [\#50](https://github.com/EMMC-ASBL/oteapi-core/issues/50)
- Rename image\_jpeg.py [\#48](https://github.com/EMMC-ASBL/oteapi-core/issues/48)
- Write unit tests [\#11](https://github.com/EMMC-ASBL/oteapi-core/issues/11)

**Merged pull requests:**

- Sg/session update model [\#78](https://github.com/EMMC-ASBL/oteapi-core/pull/78) ([sygout](https://github.com/sygout))
- New Function strategy [\#73](https://github.com/EMMC-ASBL/oteapi-core/pull/73) ([CasperWA](https://github.com/CasperWA))
- Made ResourceConfig.configuration a dict [\#67](https://github.com/EMMC-ASBL/oteapi-core/pull/67) ([jesper-friis](https://github.com/jesper-friis))
- \[Auto-generated\] Update dependencies [\#66](https://github.com/EMMC-ASBL/oteapi-core/pull/66) ([TEAM4-0](https://github.com/TEAM4-0))
- Add some dictionary functionality to configuration models [\#53](https://github.com/EMMC-ASBL/oteapi-core/pull/53) ([TorgeirUstad](https://github.com/TorgeirUstad))
- All new tests [\#35](https://github.com/EMMC-ASBL/oteapi-core/pull/35) ([TorgeirUstad](https://github.com/TorgeirUstad))

## [v0.0.5](https://github.com/EMMC-ASBL/oteapi-core/tree/v0.0.5) (2022-02-04)

[Full Changelog](https://github.com/EMMC-ASBL/oteapi-core/compare/v0.0.4...v0.0.5)

**Implemented enhancements:**

- Consider removing the `create_*_strategy()` functions [\#57](https://github.com/EMMC-ASBL/oteapi-core/issues/57)
- Lazy strategy loading [\#21](https://github.com/EMMC-ASBL/oteapi-core/issues/21)
- Extend and "safeguard" plugin loading through entry points [\#10](https://github.com/EMMC-ASBL/oteapi-core/issues/10)

**Fixed bugs:**

- Out-of-scope CVE from NumPy makes safety cry [\#54](https://github.com/EMMC-ASBL/oteapi-core/issues/54)
- pyproject.toml addopts line doesn't work on Windows [\#51](https://github.com/EMMC-ASBL/oteapi-core/issues/51)
- Ignore ID 44715 for safety [\#55](https://github.com/EMMC-ASBL/oteapi-core/pull/55) ([CasperWA](https://github.com/CasperWA))

**Merged pull requests:**

- \[Auto-generated\] Update dependencies [\#56](https://github.com/EMMC-ASBL/oteapi-core/pull/56) ([TEAM4-0](https://github.com/TEAM4-0))
- Add Windows pytest CI job [\#52](https://github.com/EMMC-ASBL/oteapi-core/pull/52) ([CasperWA](https://github.com/CasperWA))
- Start implementing entry point logic [\#47](https://github.com/EMMC-ASBL/oteapi-core/pull/47) ([CasperWA](https://github.com/CasperWA))

## [v0.0.4](https://github.com/EMMC-ASBL/oteapi-core/tree/v0.0.4) (2022-01-26)

[Full Changelog](https://github.com/EMMC-ASBL/oteapi-core/compare/v0.0.3...v0.0.4)

**Implemented enhancements:**

- Setup dependency handling via dependabot [\#31](https://github.com/EMMC-ASBL/oteapi-core/issues/31)
- Attempt simplifying strategy factory function [\#13](https://github.com/EMMC-ASBL/oteapi-core/issues/13)

**Fixed bugs:**

- Update pytest command in CI to fix codecov [\#42](https://github.com/EMMC-ASBL/oteapi-core/issues/42)
- Publish workflow failing - invoke not installed [\#40](https://github.com/EMMC-ASBL/oteapi-core/issues/40)

**Closed issues:**

- Use new TEAM 4.0\[bot\] email throughout [\#38](https://github.com/EMMC-ASBL/oteapi-core/issues/38)
- Make datacache safe to call from within a running asyncio event loop [\#26](https://github.com/EMMC-ASBL/oteapi-core/issues/26)
- Setup documentation framework [\#9](https://github.com/EMMC-ASBL/oteapi-core/issues/9)

**Merged pull requests:**

- \[Auto-generated\] Update dependencies [\#45](https://github.com/EMMC-ASBL/oteapi-core/pull/45) ([TEAM4-0](https://github.com/TEAM4-0))
- Add pytest options to pyproject.toml [\#43](https://github.com/EMMC-ASBL/oteapi-core/pull/43) ([CasperWA](https://github.com/CasperWA))
- Install the `dev` extra in publish workflow [\#41](https://github.com/EMMC-ASBL/oteapi-core/pull/41) ([CasperWA](https://github.com/CasperWA))
- Use the updated @TEAM4-0 email address [\#39](https://github.com/EMMC-ASBL/oteapi-core/pull/39) ([CasperWA](https://github.com/CasperWA))
- Implement CI/CD for dependabot [\#33](https://github.com/EMMC-ASBL/oteapi-core/pull/33) ([CasperWA](https://github.com/CasperWA))
- Remove asyncio from datacache [\#32](https://github.com/EMMC-ASBL/oteapi-core/pull/32) ([jesper-friis](https://github.com/jesper-friis))
- Setup docs framework and implement creating any strategy function [\#29](https://github.com/EMMC-ASBL/oteapi-core/pull/29) ([CasperWA](https://github.com/CasperWA))

## [v0.0.3](https://github.com/EMMC-ASBL/oteapi-core/tree/v0.0.3) (2022-01-21)

[Full Changelog](https://github.com/EMMC-ASBL/oteapi-core/compare/v0.0.2...v0.0.3)

**Implemented enhancements:**

- Remove non-"standard" strategies [\#14](https://github.com/EMMC-ASBL/oteapi-core/issues/14)
- Clean up the API [\#12](https://github.com/EMMC-ASBL/oteapi-core/issues/12)

**Fixed bugs:**

- Update CI/CD to only use Python 3.9 [\#25](https://github.com/EMMC-ASBL/oteapi-core/issues/25)
- References in README are wrong [\#18](https://github.com/EMMC-ASBL/oteapi-core/issues/18)

**Closed issues:**

- Bring back `pre-commit` [\#16](https://github.com/EMMC-ASBL/oteapi-core/issues/16)
- Publish docker image [\#15](https://github.com/EMMC-ASBL/oteapi-core/issues/15)

**Merged pull requests:**

- Updated cd\_release.yml to python 3.9 [\#28](https://github.com/EMMC-ASBL/oteapi-core/pull/28) ([kriwiik](https://github.com/kriwiik))
- Add back `pre-commit` [\#22](https://github.com/EMMC-ASBL/oteapi-core/pull/22) ([CasperWA](https://github.com/CasperWA))
- Fixed README.md References [\#20](https://github.com/EMMC-ASBL/oteapi-core/pull/20) ([anasayb](https://github.com/anasayb))
- Clean up Python API [\#17](https://github.com/EMMC-ASBL/oteapi-core/pull/17) ([CasperWA](https://github.com/CasperWA))

## [v0.0.2](https://github.com/EMMC-ASBL/oteapi-core/tree/v0.0.2) (2022-01-14)

[Full Changelog](https://github.com/EMMC-ASBL/oteapi-core/compare/beaeac12453922f381a676df7876427fa62677fe...v0.0.2)

**Implemented enhancements:**

- Release and tests CD/CI [\#1](https://github.com/EMMC-ASBL/oteapi-core/pull/1) ([CasperWA](https://github.com/CasperWA))

**Fixed bugs:**

- CD publish release workflow not working [\#4](https://github.com/EMMC-ASBL/oteapi-core/issues/4)
- CD release not working - wrong utils path [\#2](https://github.com/EMMC-ASBL/oteapi-core/issues/2)

**Merged pull requests:**

- Cleanup [\#8](https://github.com/EMMC-ASBL/oteapi-core/pull/8) ([jesper-friis](https://github.com/jesper-friis))
- Renamed oteapi/strategy-interfaces to oteapi/interfaces and updated paths in all Python modules [\#6](https://github.com/EMMC-ASBL/oteapi-core/pull/6) ([jesper-friis](https://github.com/jesper-friis))
- Update workflows to make CD work [\#5](https://github.com/EMMC-ASBL/oteapi-core/pull/5) ([CasperWA](https://github.com/CasperWA))
- Fix location of utility files for GH Actions [\#3](https://github.com/EMMC-ASBL/oteapi-core/pull/3) ([CasperWA](https://github.com/CasperWA))



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
