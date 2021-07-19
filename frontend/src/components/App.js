import React, { Component } from "react";
import { render } from "react-dom";
import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import DropdownButton from 'react-bootstrap/DropdownButton';
import Dropdown from 'react-bootstrap/Dropdown';
import NumberPicker from "react-widgets/NumberPicker";
import Button from 'react-bootstrap/Button';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      placeholder: "Loading",
      title: "Elige el curso",
      arts: [],
      art: "Elige la disciplina a asignar",
      day: 1,
      month: 4,
      year: 2021,
      hour: 23,
      minutes: 59,
      title_task: "Elija acción a realizar",
      assignment_id: 139677,
    };
    this.setCourse = this.setCourse.bind(this);
    this.makeAssigns = this.makeAssigns.bind(this);
  }

  componentDidMount() {

    fetch("api/peer_review")
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return { placeholder: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then(data => {
        this.setState(() => {
          return {
            data,
            loaded: true
          };
        });
      });

    fetch("api/arts")
    .then(response => {
      if (response.status > 400) {
        return this.setState(() => {
          return { placeholder: "Something went wrong!" };
        });
      }
      return response.json();
    })
    .then(arts => {
      this.setState(() => {
        return {
          arts,
          loaded: true
        };
      });
    });
  }

  setCourse(course) {
    this.setState(
      {
        'title': course.año + " - " + course.semestre,
        'course_id': course.id_canvas
      }
    )
    /* Guardar ID de CANVAS */
  }

  setArt(art) {
    this.setState(
      {
        'art': art.nombre
      }
    )
  }

  
  makeAssigns() {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title_task: this.state.title_task, 
                            course_id: this.state.course_id,
                            art: this.state.art,
                            assignment_id: this.state.assignment_id,
                            day: this.state.day,
                            month: this.state.month,
                            year: this.state.year,
                            hour: this.state.hour,
                            minutes: this.state.minutes })
    };
    fetch('api/make_assigns/', requestOptions)
      .then(async response => {
          const data = await response.json();
          console.log(data)
          // check for error response
          if (!response.ok) {
              // get error message from body or default to response status
              const error = (data && data.message) || response.status;
              console.log(error);
          }

          this.setState({ postId: data.id })
      })
      .catch(error => {
          this.setState({ errorMessage: error.toString() });
          console.error('There was an error!', error);
      });
  }

  render() {
    return (
      <Container>
        <Row md={4}>
          <Col></Col>
          <Col xs={6}>  
            <DropdownButton id="dropdown-courses" title={this.state.title}>
              {this.state.data.map(course => {
                return (
                  <Dropdown.Item onClick={() => this.setCourse(course)}>{course.año} - {course.semestre}</Dropdown.Item>
                );
              })}              
            </DropdownButton>
          </Col>
          <Col></Col>
        </Row>
        <Row md={4}>
          <Col></Col>
          <Col xs={6}>  
            <DropdownButton id="dropdown-arts" title={this.state.art}>
              {this.state.arts.map(art => {
                return (
                  <Dropdown.Item onClick={() => this.setArt(art)}>{art.nombre}</Dropdown.Item>
                );
              })}              
            </DropdownButton>
          </Col>
          <Col></Col>      
        </Row>
        <Row md={4}>
          <Col xs={6}>
            <label>Elige el día</label>
            <NumberPicker defaultValue={this.state.day} onChange={day => this.setState({"day": day})}/>
          </Col>
          <Col xs={6}>
            <label>Elige el mes</label>
            <NumberPicker defaultValue={this.state.month} onChange={month => this.setState({"month": month})}/>
          </Col>
          <Col xs={6}>          
            <label>Elige el año</label>
            <NumberPicker defaultValue={this.state.year} onChange={year => this.setState({"year": year})}/>
          </Col>
        </Row>
        <Row md={4}>
          <Col xs={6}>
            <label>Elige la hora</label>
            <NumberPicker defaultValue={this.state.hour} onChange={hour => this.setState({"hour": hour})}/>
          </Col>
          <Col xs={6}>
            <label>Elige los minutos</label>
            <NumberPicker defaultValue={this.state.minutes} onChange={minutes => this.setState({"minutes": minutes})}/>
          </Col>
        </Row>
        <Row md={4}>
          <Col></Col>
          <Col xs={6}>
            <label>Ingresa el ID de la tarea:</label>
            <NumberPicker defaultValue={this.state.assignment_id} onChange={assignment_id => this.setState({"assignment_id": assignment_id})}/>
          </Col>
          <Col></Col>
        </Row>
        <Row md={4}>
          <Col></Col>
          <Col>
            <DropdownButton id="dropdown-feature" title={this.state.title_task}>
              <Dropdown.Item as="button" onClick={() => this.setState({
                title_task: "Repartir ensayo"
              })}>
                Repartir ensayo
              </Dropdown.Item>
              <Dropdown.Item as="button" onClick={() => this.setState({
                title_task: "Repartir peer review"
              })}>Repartir peer review</Dropdown.Item>
            </DropdownButton>
          </Col>
        </Row>
        <Row md={4}>
          <Col></Col>
          <Col>
            <Button variant="warning" onClick={this.makeAssigns}>Confirmar elección</Button>
          </Col>
        </Row>
      </Container>
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);