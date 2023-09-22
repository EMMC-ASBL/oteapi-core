# Changelog

## [v0.5.1](https://github.com/EMMC-ASBL/oteapi-core/tree/v0.5.1) (2023-09-21)

[Full Changelog](https://github.com/EMMC-ASBL/oteapi-core/compare/v0.5.0...v0.5.1)

**Implemented enhancements:**

- Use ruff instead of pylint [\#331](https://github.com/EMMC-ASBL/oteapi-core/issues/331)
- Consider using `flit` [\#267](https://github.com/EMMC-ASBL/oteapi-core/issues/267)

**Fixed bugs:**

- Update `full_docs_dirs` input for CI/CD [\#322](https://github.com/EMMC-ASBL/oteapi-core/issues/322)

**Closed issues:**

- Revert update of codecov-action from v4 to v3 [\#328](https://github.com/EMMC-ASBL/oteapi-core/issues/328)
- Make the code-base compatible with pydantic version 2 and above [\#308](https://github.com/EMMC-ASBL/oteapi-core/issues/308)
- Document that oteapi-core must be installed editable in order to test with pytest [\#62](https://github.com/EMMC-ASBL/oteapi-core/issues/62)

**Merged pull requests:**

- Sort dependencies [\#337](https://github.com/EMMC-ASBL/oteapi-core/pull/337) ([CasperWA](https://github.com/CasperWA))
- Support pydantic v1 & v2 [\#336](https://github.com/EMMC-ASBL/oteapi-core/pull/336) ([CasperWA](https://github.com/CasperWA))
- Extend codecov uploads with strategies-specific flag [\#335](https://github.com/EMMC-ASBL/oteapi-core/pull/335) ([CasperWA](https://github.com/CasperWA))
- Use flit instead of setuptools [\#334](https://github.com/EMMC-ASBL/oteapi-core/pull/334) ([CasperWA](https://github.com/CasperWA))
- \[Auto-generated\] Update dependencies [\#333](https://github.com/EMMC-ASBL/oteapi-core/pull/333) ([TEAM4-0](https://github.com/TEAM4-0))
- Use ruff instead of pylint [\#332](https://github.com/EMMC-ASBL/oteapi-core/pull/332) ([CasperWA](https://github.com/CasperWA))
- \[Auto-generated\] Update dependencies [\#324](https://github.com/EMMC-ASBL/oteapi-core/pull/324) ([TEAM4-0](https://github.com/TEAM4-0))
- Add strategies folders to CI/CD workflows docs update [\#323](https://github.com/EMMC-ASBL/oteapi-core/pull/323) ([CasperWA](https://github.com/CasperWA))

## [v0.5.0](https://github.com/EMMC-ASBL/oteapi-core/tree/v0.5.0) (2023-09-12)

[Full Changelog](https://github.com/EMMC-ASBL/oteapi-core/compare/v0.4.5...v0.5.0)

**Fixed bugs:**

- datacache:  the hash is not updated if the value is a string [\#298](https://github.com/EMMC-ASBL/oteapi-core/issues/298)

**Closed issues:**

- Ensure all strategy models are fully expressed [\#312](https://github.com/EMMC-ASBL/oteapi-core/issues/312)
- Importing oteapi.strategies.parse.image fails for Python 3.9 [\#269](https://github.com/EMMC-ASBL/oteapi-core/issues/269)

**Merged pull requests:**

- Added support for relative file paths [\#318](https://github.com/EMMC-ASBL/oteapi-core/pull/318) ([jesper-friis](https://github.com/jesper-friis))
- \[Auto-generated\] Update dependencies [\#315](https://github.com/EMMC-ASBL/oteapi-core/pull/315) ([TEAM4-0](https://github.com/TEAM4-0))
- Fully document strategies [\#313](https://github.com/EMMC-ASBL/oteapi-core/pull/313) ([CasperWA](https://github.com/CasperWA))
- Update .pre-commit-config.yaml [\#307](https://github.com/EMMC-ASBL/oteapi-core/pull/307) ([Treesarj](https://github.com/Treesarj))
- Introduce ParserConfig Model  [\#306](https://github.com/EMMC-ASBL/oteapi-core/pull/306) ([daniel-sintef](https://github.com/daniel-sintef))
- \[Auto-generated\] Update dependencies [\#282](https://github.com/EMMC-ASBL/oteapi-core/pull/282) ([TEAM4-0](https://github.com/TEAM4-0))

## [v0.4.5](https://github.com/EMMC-ASBL/oteapi-core/tree/v0.4.5) (2023-08-11)

[Full Changelog](https://github.com/EMMC-ASBL/oteapi-core/compare/v0.4.4...v0.4.5)

**Merged pull requests:**

- update key in datacachewhen value is added as string [\#299](https://github.com/EMMC-ASBL/oteapi-core/pull/299) ([francescalb](https://github.com/francescalb))
- \[Auto-generated\] Update dependencies [\#280](https://github.com/EMMC-ASBL/oteapi-core/pull/280) ([TEAM4-0](https://github.com/TEAM4-0))
- \[Auto-generated\] Update dependencies [\#278](https://github.com/EMMC-ASBL/oteapi-core/pull/278) ([TEAM4-0](https://github.com/TEAM4-0))
- Added DOI badge to readme [\#273](https://github.com/EMMC-ASBL/oteapi-core/pull/273) ([jesper-friis](https://github.com/jesper-friis))

## [v0.4.4](https://github.com/EMMC-ASBL/oteapi-core/tree/v0.4.4) (2023-05-24)

[Full Changelog](https://github.com/EMMC-ASBL/oteapi-core/compare/v0.4.3...v0.4.4)

**Closed issues:**

- psycopg2/PostgreSQL datasource strategy [\#191](https://github.com/EMMC-ASBL/oteapi-core/issues/191)

**Merged pull requests:**

- 191 psycopg2postgresql datasource strategy [\#196](https://github.com/EMMC-ASBL/oteapi-core/pull/196) ([daniel-sintef](https://github.com/daniel-sintef))

## [v0.4.3](https://github.com/EMMC-ASBL/oteapi-core/tree/v0.4.3) (2023-05-23)

[Full Changelog](https://github.com/EMMC-ASBL/oteapi-core/compare/v0.4.2...v0.4.3)

**Merged pull requests:**

- \[Auto-generated\] Update dependencies [\#272](https://github.com/EMMC-ASBL/oteapi-core/pull/272) ([TEAM4-0](https://github.com/TEAM4-0))
- Use typing-extensions for Python \<= 3.9 [\#270](https://github.com/EMMC-ASBL/oteapi-core/pull/270) ([CasperWA](https://github.com/CasperWA))

## [v0.4.2](https://github.com/EMMC-ASBL/oteapi-core/tree/v0.4.2) (2023-05-12)

[Full Changelog](https://github.com/EMMC-ASBL/oteapi-core/compare/v0.4.1...v0.4.2)

**Implemented enhancements:**

- Update SINTEF/ci-cd [\#265](https://github.com/EMMC-ASBL/oteapi-core/issues/265)

**Fixed bugs:**

- Pin to using urllib3 v1.x [\#261](https://github.com/EMMC-ASBL/oteapi-core/issues/261)

**Closed issues:**

- Rename the pipeline get\(\) method to execute\(\) [\#250](https://github.com/EMMC-ASBL/oteapi-core/issues/250)
- Clean up requirements [\#248](https://github.com/EMMC-ASBL/oteapi-core/issues/248)
- Activate auto-merging for CI workflow to update dependencies [\#247](https://github.com/EMMC-ASBL/oteapi-core/issues/247)

**Merged pull requests:**

- Update to SINTEF/ci-cd v2 [\#266](https://github.com/EMMC-ASBL/oteapi-core/pull/266) ([CasperWA](https://github.com/CasperWA))
- \[Auto-generated\] Update dependencies [\#264](https://github.com/EMMC-ASBL/oteapi-core/pull/264) ([TEAM4-0](https://github.com/TEAM4-0))
- Pin urllib3 to v1.x [\#262](https://github.com/EMMC-ASBL/oteapi-core/pull/262) ([CasperWA](https://github.com/CasperWA))
- \[Auto-generated\] Update dependencies [\#260](https://github.com/EMMC-ASBL/oteapi-core/pull/260) ([TEAM4-0](https://github.com/TEAM4-0))
- \[Auto-generated\] Update dependencies [\#258](https://github.com/EMMC-ASBL/oteapi-core/pull/258) ([TEAM4-0](https://github.com/TEAM4-0))
- \[Auto-generated\] Update dependencies [\#256](https://github.com/EMMC-ASBL/oteapi-core/pull/256) ([TEAM4-0](https://github.com/TEAM4-0))
- \[Auto-generated\] Update dependencies [\#252](https://github.com/EMMC-ASBL/oteapi-core/pull/252) ([TEAM4-0](https://github.com/TEAM4-0))
- \[Auto-generated\] Update dependencies [\#246](https://github.com/EMMC-ASBL/oteapi-core/pull/246) ([TEAM4-0](https://github.com/TEAM4-0))
- \[Auto-generated\] Update dependencies [\#244](https://github.com/EMMC-ASBL/oteapi-core/pull/244) ([TEAM4-0](https://github.com/TEAM4-0))

## [v0.4.1](https://github.com/EMMC-ASBL/oteapi-core/tree/v0.4.1) (2023-03-10)

[Full Changelog](https://github.com/EMMC-ASBL/oteapi-core/compare/v0.4.0...v0.4.1)

**Merged pull requests:**

- \[Auto-generated\] Update dependencies [\#242](https://github.com/EMMC-ASBL/oteapi-core/pull/242) ([TEAM4-0](https://github.com/TEAM4-0))
- Polish `celery/remote` transformation strategy [\#240](https://github.com/EMMC-ASBL/oteapi-core/pull/240) ([CasperWA](https://github.com/CasperWA))
- \[Auto-generated\] Update dependencies [\#239](https://github.com/EMMC-ASBL/oteapi-core/pull/239) ([TEAM4-0](https://github.com/TEAM4-0))
- \[Auto-generated\] Update dependencies [\#235](https://github.com/EMMC-ASBL/oteapi-core/pull/235) ([TEAM4-0](https://github.com/TEAM4-0))
- \[Auto-generated\] Update dependencies [\#234](https://github.com/EMMC-ASBL/oteapi-core/pull/234) ([TEAM4-0](https://github.com/TEAM4-0))

## [v0.4.0](https://github.com/EMMC-ASBL/oteapi-core/tree/v0.4.0) (2023-02-07)

[Full Changelog](https://github.com/EMMC-ASBL/oteapi-core/compare/v0.3.0...v0.4.0)

**Fixed bugs:**

- pylint compliance [\#229](https://github.com/EMMC-ASBL/oteapi-core/issues/229)

**Closed issues:**

- Use get in transformation datamodels and celery\_remote [\#232](https://github.com/EMMC-ASBL/oteapi-core/issues/232)

**Merged pull requests:**

- Updated the interfaces and implementation of the transformation strat… [\#233](https://github.com/EMMC-ASBL/oteapi-core/pull/233) ([quaat](https://github.com/quaat))
- Move pylint config file to pyproject.toml [\#230](https://github.com/EMMC-ASBL/oteapi-core/pull/230) ([CasperWA](https://github.com/CasperWA))
- \[Auto-generated\] Update dependencies [\#228](https://github.com/EMMC-ASBL/oteapi-core/pull/228) ([TEAM4-0](https://github.com/TEAM4-0))
- \[Auto-generated\] Update dependencies [\#226](https://github.com/EMMC-ASBL/oteapi-core/pull/226) ([TEAM4-0](https://github.com/TEAM4-0))

## [v0.3.0](https://github.com/EMMC-ASBL/oteapi-core/tree/v0.3.0) (2023-01-24)

[Full Changelog](https://github.com/EMMC-ASBL/oteapi-core/compare/v0.2.1...v0.3.0)

**Implemented enhancements:**

- Add json-encoders for SecretStr/SecretByte [\#218](https://github.com/EMMC-ASBL/oteapi-core/issues/218)
- Use SINTEF/ci-cd callable workflows and pre-commit hooks [\#205](https://github.com/EMMC-ASBL/oteapi-core/issues/205)

**Fixed bugs:**

- Update configuration files for MkDocs [\#203](https://github.com/EMMC-ASBL/oteapi-core/issues/203)

**Closed issues:**

- Reenable documentation CI/CD disabled in PR \#200 [\#201](https://github.com/EMMC-ASBL/oteapi-core/issues/201)
- Error in description of MappingConfig.prefixes [\#197](https://github.com/EMMC-ASBL/oteapi-core/issues/197)
- Update pylint options [\#193](https://github.com/EMMC-ASBL/oteapi-core/issues/193)

**Merged pull requests:**

- \[Auto-generated\] Update dependencies [\#223](https://github.com/EMMC-ASBL/oteapi-core/pull/223) ([TEAM4-0](https://github.com/TEAM4-0))
- Enh/secrets json encoders [\#222](https://github.com/EMMC-ASBL/oteapi-core/pull/222) ([MBueschelberger](https://github.com/MBueschelberger))
- \[Auto-generated\] Update dependencies [\#220](https://github.com/EMMC-ASBL/oteapi-core/pull/220) ([TEAM4-0](https://github.com/TEAM4-0))
- \[Auto-generated\] Update dependencies [\#217](https://github.com/EMMC-ASBL/oteapi-core/pull/217) ([TEAM4-0](https://github.com/TEAM4-0))
- \[Auto-generated\] Update dependencies [\#215](https://github.com/EMMC-ASBL/oteapi-core/pull/215) ([TEAM4-0](https://github.com/TEAM4-0))
- \[Auto-generated\] Update dependencies [\#214](https://github.com/EMMC-ASBL/oteapi-core/pull/214) ([TEAM4-0](https://github.com/TEAM4-0))
- \[Auto-generated\] Update dependencies [\#213](https://github.com/EMMC-ASBL/oteapi-core/pull/213) ([TEAM4-0](https://github.com/TEAM4-0))
- add optional secret to functionconfig and resourceconfig [\#212](https://github.com/EMMC-ASBL/oteapi-core/pull/212) ([MBueschelberger](https://github.com/MBueschelberger))
- Updated documentation of prefixes in MappingConfig [\#209](https://github.com/EMMC-ASBL/oteapi-core/pull/209) ([jesper-friis](https://github.com/jesper-friis))
- Use SINTEF/ci-cd [\#206](https://github.com/EMMC-ASBL/oteapi-core/pull/206) ([CasperWA](https://github.com/CasperWA))
- Revert removing `--strict` and fix docs build [\#204](https://github.com/EMMC-ASBL/oteapi-core/pull/204) ([CasperWA](https://github.com/CasperWA))
- removed --strict option [\#202](https://github.com/EMMC-ASBL/oteapi-core/pull/202) ([daniel-sintef](https://github.com/daniel-sintef))
- \[Auto-generated\] Update dependencies [\#199](https://github.com/EMMC-ASBL/oteapi-core/pull/199) ([TEAM4-0](https://github.com/TEAM4-0))
- added a small clarification to the docs [\#198](https://github.com/EMMC-ASBL/oteapi-core/pull/198) ([daniel-sintef](https://github.com/daniel-sintef))
- Use recursive option for pylint-tests CI [\#194](https://github.com/EMMC-ASBL/oteapi-core/pull/194) ([CasperWA](https://github.com/CasperWA))
- \[Auto-generated\] Update dependencies [\#190](https://github.com/EMMC-ASBL/oteapi-core/pull/190) ([TEAM4-0](https://github.com/TEAM4-0))
- \[Auto-generated\] Update dependencies [\#189](https://github.com/EMMC-ASBL/oteapi-core/pull/189) ([TEAM4-0](https://github.com/TEAM4-0))
- \[Auto-generated\] Update dependencies [\#186](https://github.com/EMMC-ASBL/oteapi-core/pull/186) ([TEAM4-0](https://github.com/TEAM4-0))
- \[Auto-generated\] Update dependencies [\#184](https://github.com/EMMC-ASBL/oteapi-core/pull/184) ([TEAM4-0](https://github.com/TEAM4-0))
- \[Auto-generated\] Update dependencies [\#182](https://github.com/EMMC-ASBL/oteapi-core/pull/182) ([TEAM4-0](https://github.com/TEAM4-0))
- \[Auto-generated\] Update dependencies [\#174](https://github.com/EMMC-ASBL/oteapi-core/pull/174) ([TEAM4-0](https://github.com/TEAM4-0))

## [v0.2.1](https://github.com/EMMC-ASBL/oteapi-core/tree/v0.2.1) (2022-07-20)

[Full Changelog](https://github.com/EMMC-ASBL/oteapi-core/compare/v0.2.0...v0.2.1)

**Fixed bugs:**

- `filter/crop` not loading properly [\#170](https://github.com/EMMC-ASBL/oteapi-core/issues/170)

**Merged pull requests:**

- Test and fix registered strategies [\#171](https://github.com/EMMC-ASBL/oteapi-core/pull/171) ([CasperWA](https://github.com/CasperWA))
- \[Auto-generated\] Update dependencies [\#169](https://github.com/EMMC-ASBL/oteapi-core/pull/169) ([TEAM4-0](https://github.com/TEAM4-0))

## [v0.2.0](https://github.com/EMMC-ASBL/oteapi-core/tree/v0.2.0) (2022-07-11)

[Full Changelog](https://github.com/EMMC-ASBL/oteapi-core/compare/v0.1.6...v0.2.0)

**Implemented enhancements:**

- Implement the CSV parse strategy [\#159](https://github.com/EMMC-ASBL/oteapi-core/issues/159)

**Fixed bugs:**

- Problems accessing configurations' fields [\#113](https://github.com/EMMC-ASBL/oteapi-core/issues/113)

**Closed issues:**

- Add VIPCOAT and OpenModel to acknowledgements on all repositories. [\#133](https://github.com/EMMC-ASBL/oteapi-core/issues/133)

**Merged pull requests:**

- \[Auto-generated\] Update dependencies [\#165](https://github.com/EMMC-ASBL/oteapi-core/pull/165) ([TEAM4-0](https://github.com/TEAM4-0))
- \[Auto-generated\] Update dependencies [\#163](https://github.com/EMMC-ASBL/oteapi-core/pull/163) ([TEAM4-0](https://github.com/TEAM4-0))
- CSV parse strategy [\#160](https://github.com/EMMC-ASBL/oteapi-core/pull/160) ([CasperWA](https://github.com/CasperWA))
- \[Auto-generated\] Update dependencies [\#155](https://github.com/EMMC-ASBL/oteapi-core/pull/155) ([TEAM4-0](https://github.com/TEAM4-0))
- \[Auto-generated\] Update dependencies [\#152](https://github.com/EMMC-ASBL/oteapi-core/pull/152) ([TEAM4-0](https://github.com/TEAM4-0))
- \[Auto-generated\] Update dependencies [\#150](https://github.com/EMMC-ASBL/oteapi-core/pull/150) ([TEAM4-0](https://github.com/TEAM4-0))

## [v0.1.6](https://github.com/EMMC-ASBL/oteapi-core/tree/v0.1.6) (2022-04-20)

[Full Changelog](https://github.com/EMMC-ASBL/oteapi-core/compare/v0.1.5...v0.1.6)

**Fixed bugs:**

- Setting attributes in `AttrDict` should be handled by pydantic [\#143](https://github.com/EMMC-ASBL/oteapi-core/issues/143)

**Closed issues:**

- Add checklist for reviewers to all repositories. [\#137](https://github.com/EMMC-ASBL/oteapi-core/issues/137)

**Merged pull requests:**

- \[Auto-generated\] Update dependencies [\#149](https://github.com/EMMC-ASBL/oteapi-core/pull/149) ([TEAM4-0](https://github.com/TEAM4-0))
- Modify excel parse [\#148](https://github.com/EMMC-ASBL/oteapi-core/pull/148) ([daniel-sintef](https://github.com/daniel-sintef))
- \[Auto-generated\] Update dependencies [\#147](https://github.com/EMMC-ASBL/oteapi-core/pull/147) ([TEAM4-0](https://github.com/TEAM4-0))
- Fix deleting entries in AttrDict [\#144](https://github.com/EMMC-ASBL/oteapi-core/pull/144) ([CasperWA](https://github.com/CasperWA))
- \[Auto-generated\] Update dependencies [\#142](https://github.com/EMMC-ASBL/oteapi-core/pull/142) ([TEAM4-0](https://github.com/TEAM4-0))
- Added PR template with checklist for reviewers. [\#139](https://github.com/EMMC-ASBL/oteapi-core/pull/139) ([francescalb](https://github.com/francescalb))
- \[Auto-generated\] Update dependencies [\#136](https://github.com/EMMC-ASBL/oteapi-core/pull/136) ([TEAM4-0](https://github.com/TEAM4-0))

## [v0.1.5](https://github.com/EMMC-ASBL/oteapi-core/tree/v0.1.5) (2022-03-23)

[Full Changelog](https://github.com/EMMC-ASBL/oteapi-core/compare/v0.1.4...v0.1.5)

**Implemented enhancements:**

- Create a triple store class [\#120](https://github.com/EMMC-ASBL/oteapi-core/issues/120)
- Fix pydantic model types according to default values [\#117](https://github.com/EMMC-ASBL/oteapi-core/issues/117)

**Closed issues:**

- Fix badge links in README [\#122](https://github.com/EMMC-ASBL/oteapi-core/issues/122)

**Merged pull requests:**

- Update README.md [\#134](https://github.com/EMMC-ASBL/oteapi-core/pull/134) ([quaat](https://github.com/quaat))
- \[Auto-generated\] Update dependencies [\#130](https://github.com/EMMC-ASBL/oteapi-core/pull/130) ([TEAM4-0](https://github.com/TEAM4-0))
- triplestore class which does add, delete/update and get mappings/triples [\#128](https://github.com/EMMC-ASBL/oteapi-core/pull/128) ([Treesarj](https://github.com/Treesarj))
- Add links to badges in README [\#126](https://github.com/EMMC-ASBL/oteapi-core/pull/126) ([CasperWA](https://github.com/CasperWA))
- Fix pydantic model type and default values [\#125](https://github.com/EMMC-ASBL/oteapi-core/pull/125) ([CasperWA](https://github.com/CasperWA))

## [v0.1.4](https://github.com/EMMC-ASBL/oteapi-core/tree/v0.1.4) (2022-03-11)

[Full Changelog](https://github.com/EMMC-ASBL/oteapi-core/compare/v0.1.3...v0.1.4)

**Implemented enhancements:**

- Support passing a dictionary as config to `create_strategy()` [\#123](https://github.com/EMMC-ASBL/oteapi-core/issues/123)

**Merged pull requests:**

- Using the `StrategyType` to deliver the `*Config` cls [\#124](https://github.com/EMMC-ASBL/oteapi-core/pull/124) ([CasperWA](https://github.com/CasperWA))

## [v0.1.3](https://github.com/EMMC-ASBL/oteapi-core/tree/v0.1.3) (2022-03-10)

[Full Changelog](https://github.com/EMMC-ASBL/oteapi-core/compare/v0.1.2...v0.1.3)

**Implemented enhancements:**

- Move pytest fixtures into `oteapi` package [\#121](https://github.com/EMMC-ASBL/oteapi-core/issues/121)
- Add `pop()` \(and possibly `popitem()`\) to `AttrDict` [\#118](https://github.com/EMMC-ASBL/oteapi-core/issues/118)
- Allow to bind values added to the data cache to an object, such that they automatically will be remove when the object goes out of scope [\#114](https://github.com/EMMC-ASBL/oteapi-core/issues/114)
- Add some badges to the README [\#91](https://github.com/EMMC-ASBL/oteapi-core/issues/91)

**Fixed bugs:**

- The image strategy puts binary data in the session [\#107](https://github.com/EMMC-ASBL/oteapi-core/issues/107)

**Merged pull requests:**

- Implement and test `pop()` and `popitem()` for AttrDict [\#119](https://github.com/EMMC-ASBL/oteapi-core/pull/119) ([CasperWA](https://github.com/CasperWA))
- \[Auto-generated\] Update dependencies [\#116](https://github.com/EMMC-ASBL/oteapi-core/pull/116) ([TEAM4-0](https://github.com/TEAM4-0))
- Allow to bind the lifetime of datacache values to the lifetime of the session [\#115](https://github.com/EMMC-ASBL/oteapi-core/pull/115) ([jesper-friis](https://github.com/jesper-friis))
- Added mapping strategy [\#112](https://github.com/EMMC-ASBL/oteapi-core/pull/112) ([jesper-friis](https://github.com/jesper-friis))
- Corrected the sql\_query\_filter. [\#110](https://github.com/EMMC-ASBL/oteapi-core/pull/110) ([jesper-friis](https://github.com/jesper-friis))
- Store image data in datacache instead of session [\#108](https://github.com/EMMC-ASBL/oteapi-core/pull/108) ([jesper-friis](https://github.com/jesper-friis))
- Update README [\#106](https://github.com/EMMC-ASBL/oteapi-core/pull/106) ([CasperWA](https://github.com/CasperWA))

## [v0.1.2](https://github.com/EMMC-ASBL/oteapi-core/tree/v0.1.2) (2022-03-03)

[Full Changelog](https://github.com/EMMC-ASBL/oteapi-core/compare/v0.1.1...v0.1.2)

**Implemented enhancements:**

- Go through ignored dev tools comments [\#76](https://github.com/EMMC-ASBL/oteapi-core/issues/76)

**Fixed bugs:**

- Issue with `AttrDict.update()` for `AttrDict` subclasses [\#101](https://github.com/EMMC-ASBL/oteapi-core/issues/101)
- GH GraphQL type issue in auto-merge workflow [\#96](https://github.com/EMMC-ASBL/oteapi-core/issues/96)

**Merged pull requests:**

- Update "ignore" statements [\#103](https://github.com/EMMC-ASBL/oteapi-core/pull/103) ([CasperWA](https://github.com/CasperWA))
- Add test for AttrDict.update\(\) method [\#102](https://github.com/EMMC-ASBL/oteapi-core/pull/102) ([CasperWA](https://github.com/CasperWA))
- \[Auto-generated\] Update dependencies [\#100](https://github.com/EMMC-ASBL/oteapi-core/pull/100) ([TEAM4-0](https://github.com/TEAM4-0))
- Use `ID!` type instead of `String!` [\#97](https://github.com/EMMC-ASBL/oteapi-core/pull/97) ([CasperWA](https://github.com/CasperWA))

## [v0.1.1](https://github.com/EMMC-ASBL/oteapi-core/tree/v0.1.1) (2022-02-24)

[Full Changelog](https://github.com/EMMC-ASBL/oteapi-core/compare/v0.1.0...v0.1.1)

**Implemented enhancements:**

- Avoid registerring the incomplete `text/csv` parse strategy [\#95](https://github.com/EMMC-ASBL/oteapi-core/issues/95)
- Use special `*Config` classes where necessary [\#93](https://github.com/EMMC-ASBL/oteapi-core/issues/93)

**Closed issues:**

- Clean up the handling of paths in the file download strategy [\#84](https://github.com/EMMC-ASBL/oteapi-core/issues/84)

**Merged pull requests:**

- Update data cache invocation [\#94](https://github.com/EMMC-ASBL/oteapi-core/pull/94) ([CasperWA](https://github.com/CasperWA))
- \[Auto-generated\] Update dependencies [\#92](https://github.com/EMMC-ASBL/oteapi-core/pull/92) ([TEAM4-0](https://github.com/TEAM4-0))

## [v0.1.0](https://github.com/EMMC-ASBL/oteapi-core/tree/v0.1.0) (2022-02-22)

[Full Changelog](https://github.com/EMMC-ASBL/oteapi-core/compare/v0.0.6...v0.1.0)

**Implemented enhancements:**

- Clean up tests [\#75](https://github.com/EMMC-ASBL/oteapi-core/issues/75)
- Image parser: Use datacache [\#63](https://github.com/EMMC-ASBL/oteapi-core/issues/63)

**Fixed bugs:**

- Entrypoint does not seem to be updated during rebuild [\#86](https://github.com/EMMC-ASBL/oteapi-core/issues/86)
- Use proper file scheme URLs in tests [\#74](https://github.com/EMMC-ASBL/oteapi-core/issues/74)
- xlsx parse strategy fails parsing file on Windows [\#23](https://github.com/EMMC-ASBL/oteapi-core/issues/23)

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
