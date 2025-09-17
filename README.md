# NuGet Catalog Mirror

This repository hosts an **append-only mirror** of the official [NuGet Catalog](https://api.nuget.org/v3/catalog0/index.json).

## Sync Frequency

The mirror syncs every hour, appending new pages from the NuGet catalog. See the sync process in 
[.github/workflows/sync.yaml](.github/workflows/sync.yaml).

---

## Usage

To use the mirror, clone this repository:

```bash
git clone https://github.com/aboutcode-org/aboutcode-mirror-nuget-catalog.git
```

Once cloned, the catalog pages will be available in the `catalog/pages/` directory.

---

## License

* **Code** is licensed under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).
* **Data** is licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
