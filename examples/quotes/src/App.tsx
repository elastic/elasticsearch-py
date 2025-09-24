import React, { useRef, useState, useEffect } from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Spinner from 'react-bootstrap/Spinner';
import Stack from 'react-bootstrap/Stack';
import CloseButton from 'react-bootstrap/CloseButton';
import ToggleButton from 'react-bootstrap/ToggleButton';
import Pagination from 'react-bootstrap/Pagination';

interface Meta {
  id: string;
  score: number;
}

interface Quote {
  meta: Meta;
  quote: string;
  author: string;
  tags: string[];
};

interface Tag {
  tag: string;
  count: number;
};

export default function App() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [knn, setKnn] = useState<boolean>(true);
  const [query, setQuery] = useState<string>('');
  const [filters, setFilters] = useState<string[]>([]);
  const [tags, setTags] = useState<Tag[] | null>([]);
  const [results, setResults] = useState<Quote[] | null>(null);
  const [start, setStart] = useState<number>(0);
  const [total, setTotal] = useState<number>(0);

  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.value = query;
    }
  }, [query]);
    
  const onSearch = (ev: React.FormEvent) => {
    ev.preventDefault();
    setQuery(inputRef.current?.value || '');
    setStart(0);
  };
    
  const onResetQuery = () => {
    setQuery('');
    setStart(0);
    setTags(null);
    setResults(null);
    inputRef.current?.focus();
  };

  const onResetFilters = () => {
    setFilters([]);
    setStart(0);
    setTags(null);
    setResults(null);
    inputRef.current?.focus();
  };

  const onFilter = ({tag, count}: Tag) => {
    setFilters([...filters, tag]);
    setStart(0);
    setTags(null);
    setResults(null);
  };

  useEffect(() => {
    (async () => {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({query, filters, knn, start}),
      });
      const data: {quotes: Quote[], tags: Tag[], start: number, total: number} = await response.json();
      setResults(data.quotes);
      setTags(data.tags.filter(tag => !filters.includes(tag.tag)));
      setStart(data.start);
      setTotal(data.total);
      window.scrollTo(0, 0);
    })()
  }, [query, filters, knn, start, total]);

  return (
    <Container fluid="md" className="App">
      <Row>
        <h1>Elasticsearch + Pydantic Demo</h1>
        <Form onSubmit={onSearch} className="SearchForm">
          <Stack direction="horizontal" gap={2}>
            <Form.Control type="text" placeholder="Search for... ?" ref={inputRef} autoFocus={true} />
            <CloseButton onClick={onResetQuery} disabled={query === ''} />
            <ToggleButton id="knn" type="checkbox" variant="outline-primary" checked={knn} value="1" title="Use hybrid search" onChange={e => setKnn(e.currentTarget.checked)}>
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 256 256"><path d="M192.5,171.47A88.34,88.34,0,0,0,224,101.93c-1-45.71-37.61-83.4-83.24-85.8A88,88,0,0,0,48,102L25.55,145.18c-.09.18-.18.36-.26.54a16,16,0,0,0,7.55,20.62l.25.11L56,176.94V208a16,16,0,0,0,16,16h48a8,8,0,0,0,0-16H72V171.81a8,8,0,0,0-4.67-7.28L40,152l23.07-44.34A7.9,7.9,0,0,0,64,104a72,72,0,0,1,56-70.21V49.38a24,24,0,1,0,16,0V32c1.3,0,2.6,0,3.9.1A72.26,72.26,0,0,1,203.84,80H184a8,8,0,0,0-6.15,2.88L152.34,113.5a24.06,24.06,0,1,0,12.28,10.25L187.75,96h19.79q.36,3.12.44,6.3a72.26,72.26,0,0,1-28.78,59.3,8,8,0,0,0-3.14,7.39l8,64a8,8,0,0,0,7.93,7,8.39,8.39,0,0,0,1-.06,8,8,0,0,0,6.95-8.93ZM128,80a8,8,0,1,1,8-8A8,8,0,0,1,128,80Zm16,64a8,8,0,1,1,8-8A8,8,0,0,1,144,144Z"></path></svg>
            </ToggleButton>
          </Stack>
        </Form>
      </Row>
      <Row>
        <Col md={3} className="Tags">
          <>
            {filters != null && (
              <>
                {filters.map(tag => (
                  <div key={tag} className="Filter">
                    » {tag}
                  </div>
                ))}
                {(filters.length > 0) && (
                  <>
                    <Button variant="link" onClick={onResetFilters}>Reset</Button>
                    <hr />
                  </>
                )}
              </>
            )}
            {(tags === null) ?
              <Spinner animation="border" role="status">
                <span className="visually-hidden">Loading...</span>
              </Spinner>
            :
              <>
                {(tags.length === 0) ?
                  <p>No tags.</p>
                :
                  <>
                    {tags.map(({tag, count}) => (
                      <div key={tag} className="Tag">
                        <Button variant="link" onClick={() => onFilter({tag, count})}>{tag}</Button> ({count})
                      </div>
                    ))}
                  </>
                }
              </>
            }
          </>
        </Col>
        <Col md={9} className="Results">
          {(results === null) ?
            <Spinner animation="border" role="status">
              <span className="visually-hidden">Loading...</span>
            </Spinner>
          :
            <>
              {(results.length === 0) ?
                <p>No results. Sorry!</p>
              :
                <>
                  <p className="Summary">Showing results {start + 1}-{start + results.length} of {total}.</p>
                  {results.map(({quote, author, tags, meta}, index) => (
                    <div key={index} className="Result">
                      <p>
                        <span className="ResultQuote">{quote}</span> — <span className="ResultAuthor">{author}</span>
                        <br />
                        <span className="ResultScore">[Score: {meta.score}]</span> <span className="ResultTags">{tags.map(tag => `#${tag}`).join(', ')}</span>
                      </p>
                    </div>
                  ))}
                </>
              }
              <Pagination>
                {start > 0 && 
                  <>
                    <Pagination.First onClick={() => setStart(0)} />
                    <Pagination.Prev onClick={() => setStart(start - results.length)} />
                  </>
                }
                {results.length > 0 && start + results.length < total &&
                  <Pagination.Next onClick={() => setStart(start + results.length)} />
                }
              </Pagination>
            </>
          }
        </Col>
      </Row>
    </Container>
  );
}
