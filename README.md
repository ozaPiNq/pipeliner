# Pipeliner

Pipeliner is a task execution framework with dependencies control.

## Example

#### Write simple tasks:

```python
@task(provides=['headers', 'data', 'url'])
def fetch_url(context, url):

    # Fetch url

    context['headers'] = result.headers
    context['data'] = result.content
    context['url'] = url

@task(depends=['url', 'headers'], provides=['filename'])
def get_filename(context):
    url = context.get('url')
    headers = context.get('headers', {})

    # Check for filename in Content-Disposition header.
    # If there are no any - get filename from URL

    context['filename'] = parsed_url.path.split('/')[-1]

@task(depends=['data', 'filename'])
def save_file(context, folder, default_extension=''):
    data = context['data']
    filename = context['filename']

    # Write to file

@task(provides=['items'])
def read_file(context, input_file=''):
    # Read lines from file

    context['items'] = lines

@task(depends=['items'])
def foreach(context, func):
    """ Run Pipeline returned by func for each item. """
    items = context.get('items')

    pipelines = []
    for item in items:
        pipeline = func(item)
        pipelines.append(pipeline)
        pipeline.run()

    context.current_pipeline.wait_for(pipelines)
```

#### Create complex pipeline:

```python
def file_processing_pipeline(url):
    return Pipeline(
        fetch_url(url=url),
        get_filename(),
        save_file(folder=folder),
    )

Pipeline(
    read_file(input_file=input_file),
    foreach(file_processing_pipeline)
).run(wait=True)

```
