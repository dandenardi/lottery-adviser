# Development Notes

## Architecture Decisions

### Module Separation

The codebase follows a clean, modular architecture with clear separation of concerns:

1. **collectors/**: Responsible only for fetching data from external sources
2. **storage/**: Handles all data persistence (reading/writing Excel files)
3. **analysis/**: Pure statistical computation, no I/O or external dependencies
4. **pipelines/**: Orchestrates the workflow between modules

This separation makes the code:

- Easy to test (each module can be tested independently)
- Easy to extend (new features can be added without modifying existing code)
- Easy to understand (each module has a single, clear responsibility)

### Why No Generic Utils

The plan explicitly avoids creating a generic `utils.py` file. Instead:

- Each module contains only the functionality it needs
- Helper functions are kept close to where they're used
- This prevents the "junk drawer" problem where utils becomes a dumping ground

### Configuration Management

All paths and settings are centralized in `app/config.py`:

- Uses `pathlib.Path` for cross-platform compatibility
- Automatically creates necessary directories
- Single source of truth for all file paths

## Current Implementation Status

### ✅ Completed (Milestone 1)

- [x] Project structure created
- [x] Configuration module with path management
- [x] LotteryCollector class (placeholder for future scraping)
- [x] LotteryHistoryRepository (full Excel file management)
- [x] LotteryStatisticsService (comprehensive statistical analysis)
- [x] Pipeline orchestration
- [x] CLI entrypoint with formatted output
- [x] Sample data generator
- [x] Documentation (README, SETUP guide)

### ⏳ Pending (Future Milestones)

- [ ] Implement actual lottery scraping in `LotteryCollector`
- [ ] Add LLM-based pattern interpretation
- [ ] Strategy generation algorithms
- [ ] Simulation and backtesting framework
- [ ] Web dashboard or API
- [ ] Unit tests
- [ ] Integration tests

## Code Quality Guidelines

### Naming Conventions

- **Classes**: PascalCase (e.g., `LotteryCollector`)
- **Functions/Methods**: snake_case (e.g., `fetch_latest_result`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `PROJECT_ROOT`)
- **Private methods**: Prefix with underscore (e.g., `_validate_data`)

### Documentation

All modules, classes, and public methods include:

- Docstrings with description
- Args documentation
- Returns documentation
- Raises documentation (when applicable)
- Usage examples (when helpful)

### Error Handling

- Use specific exceptions (e.g., `FileNotFoundError`, `ValueError`)
- Provide helpful error messages with context
- Include suggestions for resolution when possible

## Testing Strategy (Future)

### Unit Tests

Each module should have corresponding unit tests:

- `tests/test_collectors.py`
- `tests/test_storage.py`
- `tests/test_analysis.py`
- `tests/test_pipelines.py`

### Integration Tests

Test the full pipeline end-to-end:

- `tests/integration/test_full_pipeline.py`

### Test Data

Use fixtures for consistent test data:

- `tests/fixtures/sample_lottery_data.xlsx`

## Performance Considerations

### Current Scale

The current implementation handles:

- ~100 contests in sample data
- Should scale to thousands of contests without issues

### Future Optimizations

If performance becomes an issue with larger datasets:

- Consider using Parquet instead of Excel for faster I/O
- Implement caching for frequently accessed statistics
- Use Dask for parallel processing of large datasets

## Extension Points

### Adding New Statistics

To add new statistical analyses:

1. Add method to `LotteryStatisticsService`
2. Update the return dictionary in `compute_statistics()`
3. Update the formatter in `scripts/run_pipeline.py`

Example:

```python
def compute_consecutive_pairs(self, history: pd.DataFrame) -> dict:
    """Analyze frequency of consecutive number pairs."""
    # Implementation here
    pass
```

### Adding New Data Sources

To add support for different lottery types:

1. Create new collector class (e.g., `PowerballCollector`)
2. Ensure it returns data in the standard format
3. Update pipeline to use the new collector

### Adding LLM Analysis

When ready to add LLM integration:

1. Create `app/llm/` module
2. Add `LLMAnalysisService` class
3. Integrate into pipeline after statistical analysis
4. Use statistics as context for LLM prompts

## Dependencies

### Core Dependencies

- **pandas**: Data manipulation and analysis
- **openpyxl**: Excel file reading/writing
- **requests**: HTTP requests (for future scraping)

### Why These Choices?

- **Pandas**: Industry standard for data analysis in Python
- **openpyxl**: Pure Python, no external dependencies, good Excel support
- **requests**: Simple, reliable HTTP library

### Future Dependencies

When implementing future features:

- **BeautifulSoup4** or **Scrapy**: For web scraping
- **OpenAI** or **Anthropic**: For LLM integration
- **FastAPI**: For REST API
- **Streamlit** or **Dash**: For web dashboard

## Deployment Considerations (Future)

### Environment Variables

When deploying, consider externalizing:

- Data file paths
- API keys (for LLM services)
- Scraping URLs

### Docker

A future Dockerfile might look like:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -e .
CMD ["python", "scripts/run_pipeline.py"]
```

## Contributing Guidelines (Future)

When opening the project to contributions:

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Run code formatters (black, ruff)
5. Submit pull request

## License

(To be determined - consider MIT or Apache 2.0)
