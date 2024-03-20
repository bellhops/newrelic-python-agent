# Copyright 2010 New Relic, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from testing_support.fixtures import (
    reset_core_stats_engine,
    validate_custom_event_count,
)

from newrelic.api.background_task import background_task


@reset_core_stats_engine()
@validate_custom_event_count(count=0)
@background_task()
def test_openai_embedding_sync(set_trace_info, sync_openai_stream_client):
    """
    Does not instrument streamed embeddings.
    """
    set_trace_info()
    with sync_openai_stream_client.embeddings.create(
        input="This is an embedding test.", model="text-embedding-ada-002"
    ) as response:
        for resp in response.iter_lines():
            assert resp


@reset_core_stats_engine()
@validate_custom_event_count(count=0)
@background_task()
def test_openai_embedding_async(loop, set_trace_info, async_openai_stream_client):
    """
    Does not instrumenting streamed embeddings.
    """
    set_trace_info()

    async def test():
        async with async_openai_stream_client.embeddings.create(
            input="This is an embedding test.", model="text-embedding-ada-002"
        ) as response:
            async for resp in response.iter_lines():
                assert resp

    loop.run_until_complete(test())


@pytest.fixture
def sync_openai_stream_client(sync_openai_client):
    return sync_openai_client.with_streaming_response


@pytest.fixture
def async_openai_stream_client(async_openai_client):
    return async_openai_client.with_streaming_response
