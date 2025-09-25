import { useState, useEffect, useRef } from 'react';
import type { MouseEvent } from 'react';
import { useParams, NavLink, useNavigate } from 'react-router';
import Container from 'react-bootstrap/Container';
import Stack from 'react-bootstrap/Stack';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Toast from 'react-bootstrap/Toast';
import ToastContainer from 'react-bootstrap/ToastContainer';
import type { Quote } from './models';

export default function Quote() {
  const [quote, setQuote] = useState<Quote | null | undefined>(undefined);
  const [status, setStatus] = useState<str>("");
  const params = useParams();
  const navigate = useNavigate();
  const quoteField = useRef<HTMLInputElement>(null);
  const authorField = useRef<HTMLInputElement>(null);
  const tagsField = useRef<HTMLInputElement>(null);

  useEffect(() => {
    (async () => {
      const response = await fetch(`/api/quotes/${params.id}`);
      const data = await response.json();
      setQuote(data);
    })();
  }, []);

  const onSubmit = async (ev: MouseEvent<HTMLElement>) => {
    ev.preventDefault();
    if (quote) {
      quote.quote = quoteField.current?.value ?? '';
      quote.author = authorField.current?.value ?? '';
      quote.tags = (tagsField.current?.value ?? "").split(',');
      let url = '/api/quotes';
      let method = 'POST';
      if (params.id !== 'new') {
        url += `/${params.id}`;
        method = 'PUT';
      }
      const response = await fetch(url, {
        method: method,
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(quote),
      });
      if (response.status == 200 || response.status == 201) {
        const data = await response.json();
        navigate(`/quotes/${data.meta.id}`);
      }
      else {
        setStatus('Save error');
      }
    }
  };

  const onDelete = async (ev: MouseEvent<HTMLElement>) => {
    ev.preventDefault();
    const response = await fetch(`/api/quotes/${params.id}`, {
      method: 'DELETE',
    });
    if (response.status == 204) {
      navigate('/');
    }
    else {
      setStatus('Delete error');
    }
  };

  return (
    <Container fluid="md" className="App">
      <h1>Elasticsearch + Pydantic Demo</h1>
      <Form className="position-relative">
        <ToastContainer position="top-end">
          <Toast bg="primary" onClose={() => setStatus('')} show={status != ''} delay={3000} autohide>
            <Toast.Body className="text-white">{status}</Toast.Body>
          </Toast>
        </ToastContainer>
        <Form.Group className="mb-3" controlId="formQuote">
          <Form.Label>Quote</Form.Label>
          <Form.Control ref={quoteField} type="text" placeholder="Enter quote" defaultValue={quote?.quote} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formAuthor">
          <Form.Label>Author</Form.Label>
          <Form.Control ref={authorField} type="text" placeholder="Enter author" defaultValue={quote?.author} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formAuthor">
          <Form.Label>Tags</Form.Label>
          <Form.Control ref={tagsField} type="text" placeholder="Enter tags" defaultValue={quote?.tags} />
        </Form.Group>
        <Stack direction="horizontal" gap={2}>
          <Button variant="primary" type="submit" onClick={onSubmit}>
            {params.id === 'new' ? 'Save' : 'Update'}
          </Button>
          {params.id !== 'new' &&
            <Button variant="danger" type="submit" onClick={onDelete}>
              Delete
            </Button>
          }
          <NavLink className="btn btn-secondary" to="/">Back</NavLink>        
        </Stack>
      </Form>
    </Container>
  );
}
